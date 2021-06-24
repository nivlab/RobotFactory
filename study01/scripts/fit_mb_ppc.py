import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv
from numba import njit
from tqdm import tqdm
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = sys.argv[1]

## Data parameters.
session = int(sys.argv[2])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and preprocess data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load data.
data = read_csv(os.path.join(ROOT_DIR,'data','data.csv'))
data.columns = [col.lower() for col in data.columns]

## Apply rejections.
reject = read_csv(os.path.join(ROOT_DIR,'data','reject.csv'))
reject.columns = [col.lower() for col in reject.columns]
data = data[data.subject.isin(reject.query('reject==0').subject)]

## Restrict sessions.
if session in [1,2,3]:
    data = data.query(f'session == {session}')
else:
    raise ValueError(f'session type = {session} not implemented.')

## Sort data.
f = lambda x: x.subject + '_' + x.rune
data['stimulus'] = np.unique(data.apply(f, 1), return_inverse=True)[-1] + 1
data['exposure'] = data.groupby(['stimulus']).exposure.transform(lambda x: np.arange(x.size)+1)
data = data.sort_values(['stimulus','exposure']).reset_index(drop=True)

## Reformat columns.
data['w1'] = np.logical_and(data.choice == 1, data.outcome == 10).astype(int)
data['w2'] = np.logical_and(data.choice == 0, data.outcome == -10).astype(int)
data['w3'] = 1 - np.logical_or(data.w1, data.w2).astype(int)
data['outcome'] = data.outcome.replace({10:1, 1:0, -1:1, -10:0})
data['valence'] = data.valence.replace({'Win':1, 'Lose':0})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
N = data.stimulus.nunique()
M = data.exposure.nunique()
J = np.unique(data.query('exposure==1').subject, return_inverse=True)[-1] + 1

## Prepare censored mappings.
C = data.pivot_table('choice','exposure','stimulus').notnull().values.astype(int)
C = np.where(data.pivot_table('rt','exposure','stimulus',dropna=False).values < 0.2, 0, C)

## Prepare task variables.
R = data.pivot_table('outcome','exposure','stimulus').fillna(0).values
V = data.pivot_table('valence','exposure','stimulus').fillna(0).values
W = data.pivot_table(['w1','w2','w3'],'stimulus','exposure').fillna(0).values.reshape(N,-1,M).T

## Prepare response variables.
Y = data.pivot_table('choice','exposure','stimulus').fillna(0).values.astype(int)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Extract parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load DataFrame.
StanFit = read_csv(os.path.join(ROOT_DIR, 'stan_results', 'mb', f'{stan_model}_s{session}.tsv.gz'), sep='\t', compression='gzip')

## Extract subject-level parameters.
b0 = StanFit.filter(regex='^b0').values
b1 = StanFit.filter(regex='^b1').values
b2 = StanFit.filter(regex='^b2').values
a1 = StanFit.filter(regex='^a1').values
a2 = StanFit.filter(regex='^a2').values
a3 = StanFit.filter(regex='^a3').values
    
## Handle nested parameters.
if not np.any(b2): b2 = b1.copy()
if not np.any(a2): a2 = a1.copy()
if not np.any(a3): a3 = a1.copy()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Posterior predictive check.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
np.random.seed(47404)

@njit
def inv_logit(x):
    return 1. / (1 + np.exp(-x))

def waic(log_lik):
    lppd = np.log( np.exp(log_lik).mean(axis=0) )
    pwaic = np.var(log_lik, axis=0)
    return lppd - pwaic

## Parameter expansion
b0_vec = b0[:,J-1]
b1_vec = b1[:,J-1]
b2_vec = b2[:,J-1]
a1_vec = a1[:,J-1]
a2_vec = a2[:,J-1]
a3_vec = a3[:,J-1]

## Generated quantities.
n_samp = b0.shape[0]
Q1 = 0.5 * b0_vec
Q2 = 0.5 * b0_vec

## Preallocate space.
Y_pred, Y_hat = np.zeros((2,N,M)) 
WAIC = np.zeros((N,M))

## Main loop.
for m in tqdm(range(M)):
    
    ## Define bias.
    bias = V[m] * b1_vec + (1-V[m]) * b2_vec
    
    ## Compute choice probability.
    theta = inv_logit( Q1 - Q2 + bias )
    
    ## Define mask.
    mask = np.where(C[m], C[m], np.nan)
    
    ## Compute choice likelihood (stage 2).
    Y_pred[:,m] = np.where(Y[m], theta, 1-theta).mean(axis=0) * mask
    
    ## Compute WAIC (stage 2).
    WAIC[:,m] = waic(np.where(Y[m], np.log(theta), np.log(1-theta))) * mask
    
    ## Simulate choice (stage 2).
    y = np.random.binomial(1, theta) * mask
    Y_hat[:,m] = y.mean(axis=0)
    
    ## Define learning rate.
    eta_vec = W[m,0] * a1_vec + W[m,1] * a2_vec + W[m,2] * a3_vec
    
    ## Update Q-values
    Q1 += Y[m] * eta_vec * ( b0_vec * R[m] - Q1 )
    Q2 += (1-Y[m]) * eta_vec * ( b0_vec * R[m] - Q2 )
    
## Store posterior predictive variables.
data = data.query('rt.isnull() or rt >= 0.2').copy()
data['Y_hat'] = Y_hat[~np.isnan(Y_hat)]
data['Y_pred'] = Y_pred[~np.isnan(Y_pred)]
data['waic'] = WAIC[~np.isnan(WAIC)]

## Restrict DataFrame to columns of interest.
cols = ['subject','session','block','trial','exposure','valence','action','robot',
        'correct','choice','rt','accuracy','sham','outcome','Y_hat','Y_pred','waic']
data = data[cols]

## Save.
f = os.path.join(ROOT_DIR, 'stan_results', 'mb', f'{stan_model}_s{session}_ppc.tsv')
data.to_csv(f, sep='\t', index=False)