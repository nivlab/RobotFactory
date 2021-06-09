import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv, get_dummies
from cmdstanpy import CmdStanModel
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'logit'

## Define session groups.
session = int(sys.argv[1])

## Define endogenous variables.
endogenous = int(sys.argv[2])

## Sampling parameters.
iter_warmup   = 1000
iter_sampling = 1000
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
if session == 1:
    data = data.query('session == 1 or session == 2')
elif session == 2:
    data = data.query('session == 1 or session == 3')
elif session == 3:
    data = data.query('session == 2 or session == 3')
else:
    raise ValueError(f'session type = {session} not implemented.')

## Restrict to participants with all data available.
data = data.groupby('subject').filter(lambda x: x.session.nunique() >= 2)

## Sort data.
data = data.sort_values(['subject','session','rune','trial']).reset_index(drop=True)

## Filter data.
data = data.query('rt.isnull() or rt >= 0.2')      # Remove fast RTs

## Reformat columns.
data['intercept'] = 1
data['valence'] = data.valence.replace({'win':1, 'lose':0})
data['action']  = data.action.replace({'go':1, 'no-go':0})
data['incongruent'] = np.logical_or(data.robot == 'NGW', data.robot == 'GAL').astype(int)
data['interaction_1'] = data.valence * data.action
data['interaction_2'] = data.valence * data.incongruent
data = data.merge(get_dummies(data.robot), left_index=True, right_index=True)

## Prepare endogenous variables.
demean = lambda x: x - np.nanmean(x)
data['valence'] = data.groupby(['subject','session']).valence.transform(demean)
data['action'] = data.groupby(['subject','session']).action.transform(demean)
data['incongruent'] = data.groupby(['subject','session']).incongruent.transform(demean)
data['interaction_1'] = data.groupby(['subject','session']).interaction_1.transform(demean)
data['interaction_2'] = data.groupby(['subject','session']).interaction_2.transform(demean)

## Prepare exogenous variables.
zscore = lambda x: (x - np.nanmean(x)) / np.nanstd(x)
data['sham'] = zscore(data.groupby(['subject','session','robot']).sham.transform(lambda x: x.mean()))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define endogenous regressors.
if endogenous == 1:
    main_effects = ['GW','NGW','GAL','NGAL']
elif endogenous == 2:
    main_effects = ['intercept','valence','action','interaction_1']
elif endogenous == 3:
    main_effects = ['intercept','valence','incongruent','interaction_2']
else:
    raise ValueError(f'endogenous type = {endogenous} not implemented.')
    
## Prepare endogenous regressors.
for i, col in enumerate(main_effects): data[f'x{i+1}'] = data[col]
X = data.filter(regex='x[0-9]').values
    
## Prepare exogenous regressors.
for i, col in enumerate(['sham']): data[f'z{i+1}'] = data[col]
Z = data.filter(regex='z[0-9]').values

## Define response variable.
Y = data.accuracy.values.astype(int)

## Define metadata.
N, M = X.shape
N, K = Z.shape
J = np.unique(data.subject, return_inverse=True)[-1] + 1
G = np.unique(data.session, return_inverse=True)[-1] + 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(N=N, M=M, K=K, J=J, G=G, Y=Y, X=X, Z=Z)

## Load StanModel
StanModel = CmdStanModel(stan_file=os.path.join(ROOT_DIR,'stan_models',f'{stan_model}.stan'))

## Fit Stan model.
StanFit = StanModel.sample(data=dd, chains=chains, iter_warmup=iter_warmup, iter_sampling=iter_sampling, thin=thin, parallel_chains=parallel_chains, seed=0, show_progress=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save samples.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
print('Saving data.')

## Define output file.
fout = f'{stan_model}_trt_s{session}_m{endogenous}'

## Extract and save Stan summary.
summary = StanFit.summary()
summary.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}_summary.tsv'), sep='\t')

## Extract and save samples.
samples = StanFit.draws_pd()
samples.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}.tsv.gz'), sep='\t', index=False, compression='gzip')