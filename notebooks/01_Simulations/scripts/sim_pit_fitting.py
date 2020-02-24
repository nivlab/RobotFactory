import os, sys, pystan
import numpy as np
from pandas import DataFrame
from scipy.stats import norm
from stantools.io import load_model
from notorious.agents import AgentsPIT

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'pit_aNP'

## Sampling parameters.
samples = 2500
warmup = 2000
chains = 4
thin = 1
n_jobs = 4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Prepare data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
np.random.seed(47404)

## Define metadata.
n = int(sys.argv[1])
K = int(sys.argv[2])
T = int(sys.argv[3])
S = 4
print(n, K, T)

## Extract parameters.
npz = np.load('params.npz')
beta, eta, tau, nu = npz['params'][n]

## Initialize agents.
agents = AgentsPIT(beta, eta, tau, nu, w=0, n_agents=1)

## Define trial parameters.
params = dict(GW  = (0.2,0.8, 0), NGW  = (0.8,0.2, 0),
              GAL = (0.2,0.8,-1), NGAL = (0.8,0.2,-1))

## Preallocate space.
Y = np.zeros((K,T,S),dtype=int)
R = np.zeros((K,T,S))

for i in range(K):

    for j, (p1, p2, s) in enumerate(params.values()):

        ## Simulate outcomes.
        r = np.random.binomial(1, (p1,p2), (1,T,2)) + s
        
        ## Simulate behavior.
        y = agents.train(r, pavlovian='V').squeeze()
        r = r.squeeze()
        
        ## Store behavior.
        R[i,:,j] = r[np.arange(T),y]
        Y[i,:,j] = y

## Assemble data.
dd = dict(K=K, S=S, T=T, Y=Y, R=R)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fit Stan Model.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
## Load StanModel
StanModel = load_model(os.path.join('stan_models',stan_model))

## Fit model.
StanFit = StanModel.sampling(data=dd, iter=samples, warmup=warmup, chains=chains, thin=thin, n_jobs=n_jobs, seed=0)

## Extract summary.
summary = StanFit.summary()
summary = DataFrame(summary['summary'], columns=summary['summary_colnames'], index=summary['summary_rownames'])

## Append parameters.
beta_pr = norm(0,1).ppf(beta / 10.)
eta_pr = norm(0,1).ppf(eta)
tau_pr = np.arctanh(tau)
nu_pr = np.arctanh(nu)

if 'trt' in stan_model:
    summary['latent'] = (beta_pr,beta_pr,eta_pr,eta_pr,tau_pr,tau_pr,nu_pr,nu_pr,beta,beta,eta,eta,tau,tau,nu,nu,0)
else:
    summary['latent'] = (beta_pr,eta_pr,tau_pr,nu_pr,beta,eta,tau,nu,0)


## Save.
summary.to_csv(os.path.join('outputs', f'{stan_model}_{n}_{K}_{T}.csv'))
