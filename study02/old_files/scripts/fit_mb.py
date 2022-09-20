import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv
from cmdstanpy import CmdStanModel
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = sys.argv[1]

## Data parameters.
session = int(sys.argv[2])

## Sampling parameters.
iter_warmup   = 5000
iter_sampling = 2500
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

## Restrict sessions.
if session in [1,2,3]:
    data = data.query(f'session == {session}')
else:
    raise ValueError(f'session type = {session} not implemented.')

## Sort data.
f = lambda x: x.subject + '_' + x.rune
data['stimulus'] = np.unique(data.apply(f, 1), return_inverse=True)[-1] + 1
data = data.sort_values(['stimulus','exposure']).reset_index(drop=True)

## Reformat columns.
data['w1'] = np.logical_and(data.choice == 1, data.outcome == 10).astype(int)
data['w2'] = np.logical_and(data.choice == 0, data.outcome == -10).astype(int)
data['w3'] = 1 - np.logical_or(data.w1, data.w2).astype(int)
data['outcome'] = data.outcome.replace({10:1, 1:0, -1:1, -10:0})
data['valence'] = data.valence.replace({'win':1, 'lose':0})

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
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(N=N, M=M, J=J, Y=Y, R=R, V=V, W=W, C=C)

## Load StanModel
StanModel = CmdStanModel(stan_file=os.path.join(ROOT_DIR,'stan_models',f'{stan_model}.stan'))

## Fit Stan model.
StanFit = StanModel.sample(data=dd, chains=chains, iter_warmup=iter_warmup, iter_sampling=iter_sampling, thin=thin, parallel_chains=parallel_chains, seed=0, show_progress=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save samples.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
print('Saving data.')

## Define output file.
fout = f'{stan_model}_s{session}'

## Extract and save Stan summary.
summary = StanFit.summary()
summary.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}_summary.tsv'), sep='\t')

## Extract and save samples.
samples = StanFit.draws_pd()
samples.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}.tsv.gz'), sep='\t', index=False, compression='gzip')