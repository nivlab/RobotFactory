import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv
from cmdstanpy import CmdStanModel, set_cmdstan_path
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = sys.argv[1]

## Data parameters.
session = sys.argv[2]

## Sampling parameters.
iter_warmup   = 2000
iter_sampling = 500
chains = 4
thin = 1
parallel_chains = 4

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
data['rune'] = data.groupby(['block','subject']).rune.transform(lambda x: np.unique(x, return_inverse=True)[-1]+1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
T = int(data.exposure.max())
H = int(data.subject.nunique() * data.rune.nunique())

## Define pivot table organization.
index = ('block','subject','robot','rune')
columns = 'exposure'

## Define data.
R = data.pivot_table('outcome',index,columns).fillna(0).values
Y = data.pivot_table('choice',index,columns).fillna(0).values.astype(int)

## Reshape data.
R = np.moveaxis(R.reshape(2,H,T).T, 2, 0)
Y = np.moveaxis(Y.reshape(2,H,T).T, 2, 0)

## Define mappings.
pivot = data.pivot_table('outcome',index,columns)
ix = pivot.index.get_level_values(0)[0]
sub_ix = np.unique(pivot.loc[ix].index.get_level_values(0), return_inverse=True)[-1] + 1
pav_ix = np.where(pivot.loc[ix].index.get_level_values(1) < 2, 1, -1)
obs_ix = np.where(np.isnan(data.pivot_table('choice',index,columns).values), 0, 1)
obs_ix = np.moveaxis(obs_ix.reshape(2,H,T).T, 2, 0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(H=H, T=T, Y=Y, R=R, sub_ix=sub_ix, obs_ix=obs_ix, pav_ix=pav_ix)

## Load StanModel
StanModel = CmdStanModel(stan_file=os.path.join(ROOT_DIR,'stan_models',f'{stan_model}.stan'))

## Fit Stan model.
StanFit = StanModel.sample(data=dd, chains=chains, iter_warmup=iter_warmup, iter_sampling=iter_sampling, thin=thin, parallel_chains=parallel_chains, seed=0, show_progress=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save samples.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
print('Saving data.')

## Extract and save Stan summary.
summary = StanFit.summary()
summary.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{stan_model}_s{session}_summary.tsv'), sep='\t')

## Extract and save samples.
samples = StanFit.draws_pd()
samples.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{stan_model}_s{session}.tsv.gz'), sep='\t', index=False, compression='gzip')
