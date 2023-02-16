import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv, concat
from cmdstanpy import CmdStanModel
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'pgng_m4_sh'
pairing = int(sys.argv[1])

## Sampling parameters.
iter_warmup   = 5000
iter_sampling = 1250
chains = 4
thin = 1
parallel_chains = 4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and prepare data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load data.
if pairing == 1:
    a = read_csv(os.path.join(ROOT_DIR, 'data', 's1', 'pgng.csv'))
    b = read_csv(os.path.join(ROOT_DIR, 'data', 's2', 'pgng.csv'))
elif pairing == 2:
    a = read_csv(os.path.join(ROOT_DIR, 'data', 's1', 'pgng.csv'))
    b = read_csv(os.path.join(ROOT_DIR, 'data', 's3', 'pgng.csv'))
elif pairing == 3:
    a = read_csv(os.path.join(ROOT_DIR, 'data', 's2', 'pgng.csv'))
    b = read_csv(os.path.join(ROOT_DIR, 'data', 's3', 'pgng.csv'))

## Merge datasets.
data = concat([a, b])

## Restrict to participants with both sessions.
data = data.groupby('subject').filter(lambda x: x.session.nunique() == 2)

## Format data.
data['valence'] = data.valence.replace({'win': 1, 'lose': 0})
data['outcome'] = np.where(data.valence, (data.outcome > 5).astype(int), (data.outcome > -5).astype(int))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
N = len(data)
J = np.unique(data.subject, return_inverse=True)[-1] + 1
K = np.unique(data.stimulus, return_inverse=True)[-1] + 1
M = np.unique(data.session, return_inverse=True)[-1] + 1

## Define data.
Y = data.choice.values.astype(int)
R = data.outcome.values.astype(int)
V = data.valence.values.astype(int)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(N=N, J=J, K=K, M=M, Y=Y, R=R, V=V)

## Load StanModel
StanModel = CmdStanModel(stan_file=os.path.join(ROOT_DIR, 'stan_models', f'{stan_model}.stan'))

## Fit Stan model.
StanFit = StanModel.sample(data=dd, chains=chains, iter_warmup=iter_warmup, iter_sampling=iter_sampling, thin=thin, parallel_chains=parallel_chains, seed=0, show_progress=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save samples.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
print('Saving data.')

## Define filename.
fout = stan_model.replace('sh',f'trt{pairing}')

## Extract and save Stan summary.
summary = StanFit.summary(percentiles=(2.5, 50, 97.5), sig_figs=3)
summary.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}_summary.tsv'), sep='\t')

## Extract and save samples.
samples = StanFit.draws_pd()
samples.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}.tsv.gz'), sep='\t', index=False, compression='gzip')