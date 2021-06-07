import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv, get_dummies
from cmdstanpy import CmdStanModel, set_cmdstan_path
set_cmdstan_path('/path/to/cmdstan')
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'logit'

## Define endogenous variables.
endogenous = int(sys.argv[1])

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

## Restrict to first 3 sessions.
data = data.query('session <= 3')

## Restrict to participants with all data available.
data = data.groupby('subject').filter(lambda x: x.session.nunique() >= 3)

## Sort data.
data = data.sort_values(['subject','session','rune','trial']).reset_index(drop=True)

## Filter data.
data = data.query('action == "go"') # Remove no-go trials
data = data.query('rt >= 0.2')      # Remove fast RTs

## Reformat columns.
data['intercept'] = 1
data['valence'] = data.valence.replace({'win':1, 'lose':0})
data = data.merge(get_dummies(data.robot), left_index=True, right_index=True)

## Prepare endogenous variables.
demean = lambda x: x - np.nanmean(x)
data['valence'] = data.groupby(['subject','session']).valence.transform(demean)

## Prepare exogenous variables (TBD).
zscore = lambda x: (x - np.nanmean(x)) / np.nanstd(x)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data for Stan.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define endogenous regressors.
if endogenous == 1:
    main_effects = ['GW','GAL']
elif endogenous == 2:
    main_effects = ['intercept','valence']
else:
    raise ValueError(f'endogenous type = {endogenous} not implemented.')
    
## Prepare endogenous regressors.
for i, (s, col) in enumerate([(s,col) for col in main_effects for s in [1,2,3]]):
    data[f'x{i+1}'] = np.where(data.session==s,1,0) * data[col]
data[f'x{i+2}'] = np.where(data.rune_set == 'bacs1', 1, 0)
data[f'x{i+3}'] = np.where(data.rune_set == 'bacs2', 1, 0)

## Prepare exogenous regressors (TBD).

## Define response variable.
Y = data.accuracy.values.astype(int)

## Define fixed-effects.
X = data.filter(regex='x[0-9]').values

## Define random-effects.
Z = X[:,:data.session.nunique() * len(main_effects)]

## Define metadata.
N, M = X.shape
N, K = Z.shape
J = np.unique(data.subject, return_inverse=True)[-1] + 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(N=N, M=M, K=K, J=J, Y=Y, X=X, Z=Z)

## Load StanModel
StanModel = CmdStanModel(stan_file=os.path.join(ROOT_DIR,'stan_models',f'{stan_model}.stan'))

## Fit Stan model.
StanFit = StanModel.sample(data=dd, chains=chains, iter_warmup=iter_warmup, iter_sampling=iter_sampling, thin=thin, parallel_chains=parallel_chains, seed=0, show_progress=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save samples.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
print('Saving data.')

## Define output file.
fout = f'{stan_model}_trt_m{endogenous}'

## Extract and save Stan summary.
summary = StanFit.summary()
summary.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}_summary.tsv'), sep='\t')

## Extract and save samples.
samples = StanFit.draws_pd()
samples.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}.tsv.gz'), sep='\t', index=False, compression='gzip')