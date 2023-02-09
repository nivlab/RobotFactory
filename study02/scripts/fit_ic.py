import os, sys
import numpy as np
from os.path import dirname
from pandas import read_csv
from cmdstanpy import CmdStanModel
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))
import json


stan_model = sys.argv[1]

## pair
i = sys.argv[2]
j = sys.argv[3]


## Sampling parameters.
iter_warmup   = 5000
iter_sampling = 2000
chains = 4
thin = 1
parallel_chains = 4


## Load data.

# Opening JSON file
r = open(os.path.join(ROOT_DIR, 'stan_data', f'ic_{i}_{j}_data.json'))

# a dictionary
dd = json.load(r)


#reformat
dd['C'] = np.array(dd['C'])
dd['S'] = np.array(dd['S'])
dd['Y'] = np.array(dd['Y'])
dd['R'] = np.array(dd['R'])
dd['V'] = np.array(dd['V'])



## Load StanModel
StanModel = CmdStanModel(stan_file=os.path.join(ROOT_DIR,'stan_models',f'trt_{stan_model}.stan'))

## Fit Stan model.
StanFit = StanModel.sample(data=dd, chains=chains, iter_warmup=iter_warmup, iter_sampling=iter_sampling, thin=thin, parallel_chains=parallel_chains, seed=0, show_progress=True)


print('Saving data.')

## Define output file.
fout = f'{stan_model}_ic_{i}_{j}'

## Extract and save Stan summary.
summary = StanFit.summary()
summary.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}_summary.tsv'), sep='\t')

## Extract and save samples.
samples = StanFit.draws_pd()
samples.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{fout}.tsv.gz'), sep='\t', index=False, compression='gzip')