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
session = sys.argv[2]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and preprocess data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load data.
data = read_csv(os.path.join(ROOT_DIR,'data','data.csv'))

## Apply rejections.
reject = read_csv(os.path.join(ROOT_DIR,'data','reject.csv'))
data = data[data.subject.isin(reject.query('reject==0').subject)]

## Restrict to one session.
data = data.query(f'session == {session}').reset_index(drop=True)

## Re-format columns.
data['robot'] = data.robot.replace({'GW':0, 'NGW':1, 'GAL':2, 'NGAL':3})
data['outcome'] = data.outcome.replace({10:1, 1:0, -1:1, -10:0})
data['rune'] = data.groupby(['subject']).rune.transform(lambda x: np.unique(x, return_inverse=True)[-1]+1)

## Re-sort data.
data = data.sort_values(['subject','robot','rune','exposure']).reset_index(drop=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
T = int(data.exposure.max())
H = int(data.subject.nunique() * data.rune.nunique())

## Define pivot table organization.
index = ('subject','robot','rune')
columns = 'exposure'

## Define data.
R = data.pivot_table('outcome',index,columns).fillna(0).values.T
Y = data.pivot_table('choice',index,columns).fillna(0).values.T.astype(int)

## Define mappings.
pivot = data.pivot_table('outcome',index,columns)
sub_ix = np.unique(pivot.index.get_level_values(0), return_inverse=True)[-1] + 1
obs_ix = np.where(np.isnan(data.pivot_table('choice',index,columns).values.T), np.nan, 1)
pav_ix = np.where(pivot.index.get_level_values(1) < 2, 1, -1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Extract parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load DataFrame.
StanFit = read_csv(os.path.join(ROOT_DIR, 'stan_results', f'{stan_model}_s{session}.tsv.gz'), sep='\t', compression='gzip')

## Extract subject-level parameters.
beta = StanFit.filter(regex='beta\[').values
eta  = StanFit.filter(regex='^eta\[').values
tau  = StanFit.filter(regex='tau\[').values
nu   = StanFit.filter(regex='nu\[').values

## Handle nested parameters.
if not np.any(tau): tau = np.zeros_like(beta)
if not np.any(nu):  nu  = np.zeros_like(beta)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Posterior predictive check.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
np.random.seed(47404)

@njit
def inv_logit(x):
    return 1. / (1 + np.exp(-x))

## Generated quantities.
n_samp = beta.shape[0]
Q1 = np.ones((n_samp, H)) * 0.5
Q2 = np.ones((n_samp, H)) * 0.5

## Parameter expansion
beta_vec = beta[:,sub_ix - 1]
eta_vec  = eta[:,sub_ix - 1]
tau_vec  = tau[:,sub_ix - 1]
nu_vec   = nu[:,sub_ix - 1]

## Preallocate space.
Y_pred, Y_hat = np.zeros((2,H,T)) 

## Main loop.
for i in tqdm(range(T)):
    
    ## Compite choice probability (stage 1).
    theta = inv_logit( beta_vec * (Q1 - Q2 + tau_vec + nu_vec * pav_ix) )
    
    ## Compute choice likelihood.
    Y_pred[:,i] = np.where(Y[i], theta, 1-theta).mean(axis=0) * obs_ix[i]
    
    ## Simulate choice.
    Y_hat[:,i] = np.random.binomial(1, theta).mean(axis=0) * obs_ix[i]
    
    ## Update action value (go)
    Q1 += Y[i] * eta_vec * (R[i] - Q1)
    
    ## Update action value (no-go)
    Q2 += (1-Y[i]) * eta_vec * (R[i] - Q2)
    
## Store posterior predictive variables.
data['Y_hat']  = Y_hat.flatten()[~np.isnan(Y_hat.flatten())]
data['Y_pred'] = Y_pred.flatten()[~np.isnan(Y_pred.flatten())]

## Save.
f = os.path.join(ROOT_DIR, 'stan_results', f'{stan_model}_s{session}_ppc.tsv.gz')
data.to_csv(f, sep='\t', compression='gzip', index=False)