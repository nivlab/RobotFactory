import os, pystan
import numpy as np
from pandas import read_csv
from anxcpt.io import load_model, load_fit, save_fit
root_dir = os.path.abspath('')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = f'pit_4arm_trt_m1'

## Sampling parameters.
samples = 3000
warmup = 2000
chains = 4
thin = 2
n_jobs = 4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Prepare data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load data.
data = read_csv('preproc.csv')

## Define metadata.
N = data.Subject.nunique()
K = data.Condition.nunique()
T = data.Trial.nunique()

## Define data.
Y = data.pivot_table('Choice',('Subject','Condition'),'Trial').astype(int).values.reshape(N,K,T)
X = data.pivot_table('Cue',('Subject','Condition'),'Trial').astype(int).values.reshape(N,K,T)
R = data.pivot_table('Outcome',('Subject','Condition'),'Trial').astype(int).values.reshape(N,K,T)

## Assemble data.
dd = dict(N=N, T=T, Y=Y, X=X, R=R)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
## Load StanModel
StanModel = load_model(os.path.join('stan_models',stan_model))

## Fit model.
StanFit = StanModel.sampling(data=dd, iter=samples, warmup=warmup, chains=chains, thin=thin, n_jobs=n_jobs, seed=0)

## Save.
f = os.path.join(root_dir, stan_model)
save_fit(f, StanFit, data=dd)
