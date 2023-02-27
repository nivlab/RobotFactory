import os, sys
import numpy as np
from os.path import dirname
from pandas import DataFrame, read_csv
from tqdm import tqdm
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))
np.random.seed(47404)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = sys.argv[1]
sessions = ['s1','s2','s3']
pairings = [1,2,3]

## Bootstrap parameters.
params = ['b1','b2','b3','b4','a1','a2','c1']
n_shuffle = 5000
bounds = [2.5, 97.5]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Split-half reliability.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Preallocate space.
reliability = []

## Iterate over parameters.
for param in tqdm(params):

    ## Preallocate space.
    rho = []
    rho_null = []
    
    ## Iterate over sessions.
    for session in sessions:
    
        ## Load Stan summary.
        f = os.path.join(ROOT_DIR, 'stan_results', session, f'{stan_model}_sh_summary.tsv')
        summary = read_csv(f, sep='\t', index_col=0)
        
        ## Extract parameter.
        arr = summary.T.filter(regex=f'{param}\[').T['Mean'].values.reshape(-1,2)
        if not np.any(arr): continue

        ## Compute reliability (observed).
        rho.append(np.corrcoef(arr.T)[0,1])
        
        ## Compute reliability (shuffled).
        null = []
        for _ in range(n_shuffle):
            ix = np.random.choice(np.arange(len(arr)), len(arr), replace=True)
            null.append(np.corrcoef(arr[ix].T)[0,1])
        rho_null.append(null)
        
    ## Error-catching: assert parameter in model.
    if not np.any(rho): continue
        
    ## Compute confidence intervals.
    lbs, ubs = np.percentile(rho_null, bounds, axis=1)
    
    ## Compute grand average.
    mu = np.mean(rho)
    lb, ub = np.percentile(np.mean(rho_null, axis=0), bounds)
    
    ## Append info.
    reliability.append({'Param': param, 'Type': 'sh', 'Group': 0, 'Mean': mu, f'{bounds[0]}%': lb, f'{bounds[1]}%': ub})
    for i, (mu, lb, ub) in enumerate(zip(rho, lbs, ubs)):
        reliability.append({'Param': param, 'Type': 'sh', 'Group': i+1, 'Mean': mu, f'{bounds[0]}%': lb, f'{bounds[1]}%': ub})
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Test-retest reliability.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Iterate over parameters.
for param in tqdm(params):

    ## Preallocate space.
    rho = []
    rho_null = []
    
    ## Iterate over sessions.
    for pair in pairings:
    
        ## Load Stan summary.
        f = os.path.join(ROOT_DIR, 'stan_results', f'{stan_model}_trt{pair}_summary.tsv')
        summary = read_csv(f, sep='\t', index_col=0)
        
        ## Extract parameter.
        arr = summary.T.filter(regex=f'{param}\[').T['Mean'].values.reshape(-1,2)
        if not np.any(arr): continue
        
        ## Compute reliability (observed).
        rho.append(np.corrcoef(arr.T)[0,1])
        
        ## Compute reliability (shuffled).
        null = []
        for _ in range(n_shuffle):
            ix = np.random.choice(np.arange(len(arr)), len(arr), replace=True)
            null.append(np.corrcoef(arr[ix].T)[0,1])
        rho_null.append(null)
        
    ## Error-catching: assert parameter in model.
    if not np.any(rho): continue
        
    ## Compute confidence intervals.
    lbs, ubs = np.percentile(rho_null, bounds, axis=1)
    
    ## Compute grand average.
    mu = np.mean(rho)
    lb, ub = np.percentile(np.mean(rho_null, axis=0), bounds)
    
    ## Append info.
    reliability.append({'Param': param, 'Type': 'trt', 'Group': 0, 'Mean': mu, f'{bounds[0]}%': lb, f'{bounds[1]}%': ub})
    for i, (mu, lb, ub) in enumerate(zip(rho, lbs, ubs)):
        reliability.append({'Param': param, 'Type': 'trt', 'Group': i+1, 'Mean': mu, f'{bounds[0]}%': lb, f'{bounds[1]}%': ub})
        
## Convert to DataFrame.
reliability = DataFrame(reliability)

## Format data.
cols = reliability.columns[np.in1d(reliability.dtypes, [np.float16, np.float32, np.float64])]
reliability[cols] = reliability[cols].round(6)

## Save data.
reliability.to_csv(os.path.join(ROOT_DIR, 'stan_results', f'{stan_model}_reliability.csv'), index=False)