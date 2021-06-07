import os, sys, pystan
import numpy as np
from pandas import read_csv, get_dummies
from notorious.io import load_model, save_fit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'logistic_trt'

## Sampling parameters.
samples = 2500
warmup = 2000
chains = 4
thin = 1
n_jobs = 4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and preprocess data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load data.
data = read_csv(os.path.join('data','bennett2020.csv'))

## Reformat columns.
f = lambda x: np.arange(x.size) + 1
data['stimulus_type'] = data.stimulus_type.replace({'GW':0, 'NGW':1, 'GAL':2, 'NGAL':3})
data['block'] = np.where(data['block'] < 4, 1, 2)
data['trial'] = data.groupby(['id','block']).trial.transform(f)

## Define dummy coded stimulus condition.
data[[0,1,2,3]] = get_dummies(data.stimulus_type)

## Restrict to participants with GW accuracy > 0.5.
gb = data.query('stimulus_type==0').groupby('id').correct.mean()
data = data[data.id.isin(gb[gb>0.5].index)]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
N = data.id.nunique()
T = data.trial.max()

## Define data.
X = data.pivot_table([0,1,2,3],['id','block'],'trial').values.reshape(N,2,-1,T).swapaxes(2,3)
Y = data.pivot_table('action',('id','block'),'trial').values.reshape(N,2,-1)

## Assemble data.
dd = dict(N=N, T=T, X=X, Y=Y)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
## Load StanModel
StanModel = load_model(os.path.join('stan_models',stan_model))

## Fit model.
StanFit = StanModel.sampling(data=dd, iter=samples, warmup=warmup, chains=chains, 
                             thin=thin, n_jobs=n_jobs, seed=47404)

## Save.
f = os.path.join(stan_model)
save_fit(f, StanFit, data=dd)