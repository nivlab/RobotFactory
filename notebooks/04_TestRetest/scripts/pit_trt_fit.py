import os, sys, pystan
import numpy as np
from pandas import read_csv
from notorious.io import load_model, save_fit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
data_file  = 'bennett2020.csv'
stan_model = 'pit_trt_m1'

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
data = read_csv(data_file)

## Reformat columns.
f = lambda x: np.arange(x.size) + 1
data['stimulus_type'] = data.stimulus_type.replace({'GW':0, 'NGW':1, 'GAL':2, 'NGAL':3})
data['block'] = np.where(data['block'] < 4, 1, 2)
data['exposure'] = data.groupby(['id','block','stimulus_type']).trial.transform(f)

## Restrict to participants with GW accuracy > 0.5.
gb = data.query('stimulus_type==0').groupby('id').correct.mean()
data = data[data.id.isin(gb[gb>0.5].index)]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
T = data.exposure.max()
H = data.id.nunique() * data.stimulus_type.nunique()

## Define data.
R = data.pivot_table('feedback',('block','id','stimulus_type'),'exposure').values
Y = data.pivot_table('action',('block','id','stimulus_type'),'exposure').values

## Reshape data.
R = np.moveaxis(R.reshape(2,H,T).T, 2, 0)
Y = np.moveaxis(Y.reshape(2,H,T).T, 2, 0)

## Define mappings.
pivot = data.pivot_table('action',('id','stimulus_type'),'exposure')
sub_ix = np.unique(pivot.index.get_level_values(0), return_inverse=True)[-1] + 1
pav_ix = np.where(pivot.index.get_level_values(1) < 2, 1, -1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(H=H, T=T, Y=Y, R=R, sub_ix=sub_ix, pav_ix=pav_ix)
    
## Load StanModel
StanModel = load_model(os.path.join('stan_models',stan_model))

## Fit model.
StanFit = StanModel.sampling(data=dd, iter=samples, warmup=warmup, chains=chains, 
                             thin=thin, n_jobs=n_jobs, seed=47404)

## Save.
f = os.path.join(stan_model)
save_fit(f, StanFit, data=dd)