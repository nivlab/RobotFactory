import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv
from psis import psisloo
from tqdm import tqdm
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = sys.argv[1]
session = sys.argv[2]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and prepare data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load data.
data = read_csv(os.path.join(ROOT_DIR, 'data', session, 'pgng.csv'))

## Restrict participants.
if session == 's1':
    reject = read_csv(os.path.join(ROOT_DIR, 'data', session, 'reject.csv'))
    data = data[data.subject.isin(reject.query('reject==0').subject)].reset_index(drop=True)

## Format data.
data['valence'] = data.valence.replace({'win': 1, 'lose': 0})
data['outcome'] = np.where(data.valence, (data.outcome > 5).astype(int), (data.outcome > -5).astype(int))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
N = len(data)
J = np.unique(data.subject, return_inverse=True)[-1]
K = np.unique(data.stimulus, return_inverse=True)[-1]
M = np.unique(data.block, return_inverse=True)[-1]

## Define data.
Y = data.choice.values.astype(int)
R = data.outcome.values.astype(int)
V = data.valence.values.astype(int)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Extract parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load DataFrame.
StanFit = read_csv(os.path.join(ROOT_DIR, 'stan_results', session, f'{stan_model}.tsv.gz'), sep='\t', compression='gzip')

## Extract subject-level parameters.
b1 = StanFit.filter(regex='b1\[').values
b2 = StanFit.filter(regex='b2\[').values
b3 = StanFit.filter(regex='b3\[').values
b4 = StanFit.filter(regex='b3\[').values
a1 = StanFit.filter(regex='a1\[').values
a2 = StanFit.filter(regex='a2\[').values
a3 = StanFit.filter(regex='a3\[').values

## Handle missing parameters.
if not np.any(b2): b2 = np.zeros_like(b1)
if not np.any(b3): b3 = np.zeros_like(b1)
if not np.any(b4): b4 = np.zeros_like(b1)
if not np.any(a2): a2 = a1.copy()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Posterior predictive check.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
np.random.seed(47404)

def inv_logit(x):
    return 1. / (1 + np.exp(-x))

## Initialize Q-values.
n_samp = len(StanFit)
Q = np.ones((n_samp, J.max()+1, K.max()+1, 2)) * 0.5
C = np.ones((J.max()+1, K.max()+1, 2)) * 0.5

## Preallocate space.
Y_hat, Y_pred = np.zeros((2,N))
cll = np.zeros((n_samp, N))

## Main loop.
for n in tqdm(range(N)):
    
    ## Compite linear predictor.
    mu = b1[:,J[n]] * (Q[:,J[n],K[n],1] - Q[:,J[n],K[n],0]) + b2[:,J[n]] + b3[:,J[n]] * V[n] +\
         b4[:,J[n]] * (C[J[n],K[n],1] - C[J[n],K[n],0])
    p = inv_logit(mu)
    
    ## Simulate choice.
    Y_hat[n] = np.random.binomial(1, p).mean(axis=0)
    
    ## Compute choice likelihood.
    cll[:,n] = np.where(Y[n], p, 1-p)
    Y_pred[n] = cll[:,n].mean(axis=0)
    
    ## Compute prediction error.
    delta = R[n] - Q[:,J[n],K[n],Y[n]]
    
    ## Assign learning rate.
    if not np.any(a3):
        eta = V[n] * a1[:,J[n]] + (1-V[n]) * a2[:,J[n]]
    else:
        if (V[n] == 1) and (R[n] == 1):
            eta = a1[:,J[n]]
        elif (V[n] == 0) and (R[n] == 0):
            eta = a2[:,J[n]]
        else:
            eta = a3[:,J[n]]
    
    ## Update Q-values
    Q[:,J[n],K[n],Y[n]] += eta * delta
    
    ## Update C-values
    C[J[n],K[n],1] += (Y[n] - C[J[n],K[n],1])
    C[J[n],K[n],0] += ((1-Y[n]) - C[J[n],K[n],0])
    
## Store posterior predictive variables.
data['Y_hat'] = Y_hat.round(6)
data['Y_pred'] = Y_pred.round(6)

## Compute p_waic (effective number of parameters).
pwaic = cll.var(axis=0)

## Compute PSIS-LOO.
loo, loos, ku = psisloo(cll)
data['pwaic'] = pwaic.round(6)
data['loo'] = loos.round(6)
data['k_u'] = ku.round(6)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Restrict DataFrame to columns of interest.
cols = ['subject','session','block','runsheet','trial','exposure','stimulus','valence','action',
        'robot','choice','accuracy','rt','outcome','Y_hat','Y_pred','pwaic','k_u','loo']
data = data[cols]

## Sort DataFrame.
data = data.sort_values(['subject','session','stimulus','exposure']).reset_index(drop=True)

## Save.
f = os.path.join(ROOT_DIR, 'stan_results', session, f'{stan_model}_ppc.csv')
data.to_csv(f, index=False)