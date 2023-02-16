import os, sys
import numpy as np
from os.path import dirname
from pandas import Categorical, read_csv, concat, get_dummies
from cmdstanpy import CmdStanModel
from statsmodels.api import Logit
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'logit'
ipw = int(sys.argv[1])

## Sampling parameters.
iter_warmup   = 2000
iter_sampling = 500
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

## Sort data.
data = data.sort_values(['subject','session','trial']).reset_index(drop=True)

## Format data.
normalize = lambda x: (x - x.min()) / (x.max() - x.min())
data['action'] = data.action.replace({'go': 0.5, 'no-go': -0.5})
data['valence'] = data.valence.replace({'win': 0.5, 'lose': -0.5})
data['exposure'] = normalize(data.exposure) - 0.5

## Define inverse-probability weighting (by rune set).
if ipw:
    
    ## Calculate inverse-probability weights (i.e., number of participants exposed to rune set by session).
    data['rune_w'] = data.groupby(['rune_set','session']).subject.transform(lambda x: 1. / x.nunique())
    
    ## Normalize weights (mean = 1).
    data['rune_w'] = data.groupby('rune_set').rune_w.transform(lambda x: x / x.unique().mean())
    
else:
    
    ## Fix weights to one.
    data['rune_w'] = 1

## Define predictors.
data['x11'] = 1
data['x12'] = data.action.values
data['x13'] = data.valence.values
data['x14'] = data.action.values * data.valence.values * 2
data['x15'] = data.exposure.values
data[[f'x2{i+1}' for i in range(3)]] = get_dummies(data.rune_set).values * data.rune_w.values.reshape(-1,1)

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
### Calculate initial values.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define convenience function.
def fit_mvlr(data, formula, method='lbfgs', maxiter=1000):
    """Fit multivariate logistic regression model."""
    fit = Logit.from_formula(formula, data=data).fit(method=method, maxiter=maxiter, disp=0)
    return fit.params
    
## Define formula.
formula = 'accuracy ~ ' + ' + '.join(data.filter(regex='x1').columns) + ' - 1'

## Fit model (to each participant / session individually).
order = [Categorical(data.subject), Categorical(data.session)]
betas = data.groupby(order).apply(fit_mvlr, formula=formula).reset_index()

## Fill missing values.
cols = betas.filter(regex='x1').columns
betas[cols] = betas.groupby(['level_0'])[cols].transform(lambda x: x.fillna(x.mean()))

## Reshape values.
betas = np.rollaxis(betas[cols].values.reshape(J.max(), K.max(), M1), -1)

## Calculate grand averages / demean values.
beta_mu_01 = np.array([np.mean(arr) for arr in betas])
beta_pr = betas - beta_mu_01.reshape(-1,1,1)

## Calculate standard deviations / standardize values.
sigma = np.array([np.std(arr) for arr in beta_pr])
beta_pr = beta_pr / sigma.reshape(-1,1,1)

## Define between-participant effects.
beta_mu_02_pr = np.zeros(M2 - 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Assemble data.
dd = dict(N=N, M1=M1, M2=M2, J=J, K=K, Y=Y, X1=X1, X2=X2)

## Assemble initial values.
inits = dict(beta_mu_01=beta_mu_01, beta_mu_02_pr=beta_mu_02_pr, sigma=sigma, beta_pr=beta_pr)

## Load StanModel
StanModel = CmdStanModel(stan_file=os.path.join(ROOT_DIR, 'stan_models', f'{stan_model}.stan'))

## Fit Stan model.
StanFit = StanModel.sample(data=dd, chains=chains, iter_warmup=iter_warmup, iter_sampling=iter_sampling, thin=thin, parallel_chains=parallel_chains, inits=inits, seed=0, show_progress=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save samples.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define fout.
fout = os.path.join(ROOT_DIR, 'stan_results', f'{stan_model}_m{ipw}')
    
## Extract summary and samples.
summary = StanFit.summary(percentiles=(2.5, 50, 97.5), sig_figs=3)
samples = StanFit.draws_pd()
    
## Define columns to save.
cols = np.concatenate([
    
    ## Diagnostic variables.
    samples.filter(regex='__').columns,
    
    ## Regression effects (population-level).
    samples.filter(regex='beta_mu_0[1-2]\[').columns,
        
    ## Variances (group-level).
    samples.filter(regex='sigma').columns,
    
    ## Regression effects (group-level).
    samples.filter(regex='beta\[').columns,
    
])
    
## Save.
samples[cols].to_csv(f'{fout}.tsv.gz', sep='\t', index=False, compression='gzip')
summary.loc[samples[cols].filter(regex='[^_]$').columns].to_csv(f'{fout}_summary.tsv', sep='\t')