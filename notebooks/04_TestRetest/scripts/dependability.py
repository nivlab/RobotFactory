import os, sys, h5py
import numpy as np
import pystan
from os.path import dirname
from pandas import DataFrame, read_csv
from notorious.io import load_model
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))
arg1 = sys.argv[1]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## IO parameters.
stan_model = 'pit_trt_m1'

## Sampling parameters.
samples = 5000
warmup = 4000
chains = 4
thin = 1
n_jobs = 4

## Metadata parameters.
session = arg1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and preprocess data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load data.
data = read_csv(os.path.join(ROOT_DIR,'data','data.csv'))

## Apply rejections.
reject = read_csv(os.path.join(ROOT_DIR,'data','reject.csv'))
data = data[~data.Subject.isin(reject.query('Reject == 1').Subject)].reset_index(drop=True)

## Restrict to single session.
data = data.query(f'Session == {arg1}')

## Reformat columns.
f = lambda x: np.arange(x.size) + 1
data['Robot'] = data.Robot.replace({'GW':0, 'NGW':1, 'GAL':2, 'NGAL':3})
data['Exposure'] = data.groupby(['Subject','Block','Robot']).Trial.transform(f)
data['Outcome'] = data.Outcome.replace({10:1, 1:0, -1:0, -10:-1})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
T = data.Exposure.max()
H = data.Subject.nunique() * data.Robot.nunique()

## Define data.
R = data.pivot_table('Outcome',('Block','Subject','Robot'),'Exposure').values
Y = data.pivot_table('Choice',('Block','Subject','Robot'),'Exposure').values

## Reshape data.
R = np.moveaxis(R.reshape(2,H,T).T, 2, 0)
Y = np.moveaxis(Y.reshape(2,H,T).T, 2, 0)

## Define mappings.
pivot = data.pivot_table('Choice',('Subject','Robot'),'Exposure')
sub_ix = np.unique(pivot.index.get_level_values(0), return_inverse=True)[-1] + 1
pav_ix = np.where(pivot.index.get_level_values(1) < 2, 1, -1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(H=H, T=T, Y=Y, R=R, sub_ix=sub_ix, pav_ix=pav_ix)
    
## Load StanModel
StanModel = load_model(os.path.join(ROOT_DIR,'stan_models',stan_model))

## Fit model.
StanFit = StanModel.sampling(data=dd, iter=samples, warmup=warmup, chains=chains, thin=thin, n_jobs=n_jobs, seed=0)

## Extract samples.
StanDict = StanFit.extract()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define output paths.
filepath = os.path.join(ROOT_DIR,'stan_results',f'dependability_t{session}')

## Save summary file.
summary = StanFit.summary()
summary = DataFrame(summary['summary'], columns=summary['summary_colnames'], index=summary['summary_rownames'])
summary.to_csv(filepath+'.csv')

## Save data.
with h5py.File(f'{filepath}.hdf5', 'w') as f:
    
    ## Iteratively add observed data.
    for k, v in dd.items():
        f.create_dataset(k, data=v)
        
    ## Iteratively add Stan samples.
    for k, v in StanDict.items():
        if k == 'lp__': continue
        f.create_dataset(k, data=v)