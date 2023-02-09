import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv, concat, get_dummies
from cmdstanpy import CmdStanModel
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'logit'

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
data = concat([read_csv(os.path.join(ROOT_DIR, 'data', session, 'pgng.csv'))
               for session in ['s1','s2','s3']])

## Restrict participants.
reject = read_csv(os.path.join(ROOT_DIR, 'data', 's1', 'reject.csv'))
data = data[data.subject.isin(reject.query('reject==0').subject)].reset_index(drop=True)

## Format data.
normalize = lambda x: (x - x.min()) / (x.max() - x.min())
data['action'] = data.action.replace({'go': 0.5, 'no-go': -0.5})
data['valence'] = data.valence.replace({'win': 0.5, 'lose': -0.5})
data['exposure'] = normalize(data.exposure) - 0.5

## Define predictors.
data['x11'] = 1
data['x12'] = data.action.values
data['x13'] = data.valence.values
data['x14'] = data.action.values * data.valence.values * 2
data['x15'] = data.exposure.values
data['x21'] = np.where(data['rune_set'] == 'bacs1', 1, 0)
data['x22'] = np.where(data['rune_set'] == 'bacs2', 1, 0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
N = len(data)
M1 = len(data.filter(regex='x1[0-9]').T)
M2 = len(data.filter(regex='x2[0-9]').T)
J = np.unique(data.subject, return_inverse=True)[-1] + 1
K = np.unique(data.session, return_inverse=True)[-1] + 1

## Define data.
Y = data.accuracy.values.astype(int)

## Define design matrix.
X1 = data.filter(regex='x1[0-9]').values
X2 = data.filter(regex='x2[0-9]').values

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(N=N, M1=M1, M2=M2, J=J, K=K, Y=Y, X1=X1, X2=X2)

## Load StanModel
StanModel = CmdStanModel(stan_file=os.path.join(ROOT_DIR, 'stan_models', f'{stan_model}.stan'))

## Fit Stan model.
StanFit = StanModel.sample(data=dd, chains=chains, iter_warmup=iter_warmup, iter_sampling=iter_sampling, thin=thin, parallel_chains=parallel_chains, seed=0, show_progress=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save samples.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define fout.
fout = os.path.join(ROOT_DIR, 'stan_results', stan_model)
    
## Extract summary and samples.
summary = StanFit.summary(percentiles=(2.5, 50, 97.5), sig_figs=3)
samples = StanFit.draws_pd()
    
## Define columns to save.
cols = np.concatenate([
    
    ## Diagnostic variables.
    samples.filter(regex='__').columns,
    
    ## Regression effects (population-level).
    samples.filter(regex='beta_mu').columns,
    
    ## Regression effects (group-level).
    samples.filter(regex='beta\[').columns,
    
    ## Variances.
    samples.filter(regex='sigma').columns,
    
])
    
## Save.
samples[cols].to_csv(f'{fout}.tsv.gz', sep='\t', index=False, compression='gzip')
summary.loc[samples[cols].filter(regex='[^_]$').columns].to_csv(f'{fout}_summary.tsv', sep='\t')