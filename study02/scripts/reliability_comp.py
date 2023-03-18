import os, sys
import numpy as np
from os.path import dirname
from pandas import DataFrame, read_csv
from tqdm import tqdm
ROOT_DIR = dirname(dirname(dirname(os.path.realpath(__file__))))
np.random.seed(47404)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## I/O parameters.
stan_model = 'pgng_m7'
sessions = ['s1','s2','s3']
pairings = [1,2,3]

## Bootstrap parameters.
params = ['b1','b2','b3','b4','a1','a2','c1']
n_shuffle = 500
bounds = [2.5, 97.5]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Split-half reliability.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Preallocate space.
reliability = []

## Iterate over parameters.
for param in tqdm(params):
    
    ## Preallocate space.
    delta = []
    delta_null = []
    
    ## Iterate over sessions.
    for session in sessions:
    
        ## Load Stan summary.
        f1 = os.path.join(ROOT_DIR, 'study01', 'stan_results', session, f'{stan_model}_sh_summary.tsv')
        s1 = read_csv(f1, sep='\t', index_col=0)
        f2 = os.path.join(ROOT_DIR, 'study02', 'stan_results', session, f'{stan_model}_sh_summary.tsv')
        s2 = read_csv(f2, sep='\t', index_col=0)
        
        ## Extract parameter.
        a = s1.T.filter(regex=f'{param}\[').T['Mean'].values.reshape(-1,2)
        b = s2.T.filter(regex=f'{param}\[').T['Mean'].values.reshape(-1,2)
        if not np.any(a): continue
        
        ## Compute reliability (observed).
        delta.append(np.corrcoef(b.T)[0,1] - np.corrcoef(a.T)[0,1])
        
        ## Compute reliability (bootstrapped).
        null = []
        for _ in range(n_shuffle):
            ix1 = np.random.choice(np.arange(len(a)), len(a), replace=True)
            ix2 = np.random.choice(np.arange(len(b)), len(b), replace=True)
            null.append(np.corrcoef(b[ix2].T)[0,1] - np.corrcoef(a[ix1].T)[0,1])
        delta_null.append(null)
            
        ## Compute bounds.
        lb, ub = np.percentile(null, bounds)
        
    ## Error-catching: assert parameter in model.
    if not np.any(delta): continue
        
    ## Compute confidence intervals.
    lbs, ubs = np.percentile(delta_null, bounds, axis=1)
    
    ## Compute grand average.
    mu = np.mean(delta)
    lb, ub = np.percentile(np.mean(delta_null, axis=0), bounds)
    
    ## Append info.
    reliability.append({'Param': param, 'Type': 'sh', 'Group': 0, 'Mean': mu, f'{bounds[0]}%': lb, f'{bounds[1]}%': ub})
    for i, (mu, lb, ub) in enumerate(zip(delta, lbs, ubs)):
        reliability.append({'Param': param, 'Type': 'sh', 'Group': i+1, 'Mean': mu, f'{bounds[0]}%': lb, f'{bounds[1]}%': ub})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Test-retest reliability.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Iterate over parameters.
for param in tqdm(params):
    
    ## Preallocate space.
    delta = []
    delta_null = []
    
    ## Iterate over sessions.
    for pair in pairings:
    
        ## Load Stan summary.
        s1 = read_csv(os.path.join(ROOT_DIR, 'study01', 'stan_results', f'{stan_model}_trt{pair}_summary.tsv'), 
                      sep='\t', index_col=0)
        s2 = read_csv(os.path.join(ROOT_DIR, 'study02', 'stan_results', f'{stan_model}_trt{pair}_summary.tsv'), 
                      sep='\t', index_col=0)
        
        ## Extract parameter.
        a = s1.T.filter(regex=f'{param}\[').T['Mean'].values.reshape(-1,2)
        b = s2.T.filter(regex=f'{param}\[').T['Mean'].values.reshape(-1,2)
        if not np.any(a): continue
        
        ## Compute reliability (observed).
        delta.append(np.corrcoef(b.T)[0,1] - np.corrcoef(a.T)[0,1])
        
        ## Compute reliability (bootstrapped).
        null = []
        for _ in range(n_shuffle):
            ix1 = np.random.choice(np.arange(len(a)), len(a), replace=True)
            ix2 = np.random.choice(np.arange(len(b)), len(b), replace=True)
            null.append(np.corrcoef(b[ix2].T)[0,1] - np.corrcoef(a[ix1].T)[0,1])
        delta_null.append(null)
            
        ## Compute bounds.
        lb, ub = np.percentile(null, bounds)
        
    ## Error-catching: assert parameter in model.
    if not np.any(delta): continue
        
    ## Compute confidence intervals.
    lbs, ubs = np.percentile(delta_null, bounds, axis=1)
    
    ## Compute grand average.
    mu = np.mean(delta)
    lb, ub = np.percentile(np.mean(delta_null, axis=0), bounds)
    
    ## Append info.
    reliability.append({'Param': param, 'Type': 'trt', 'Group': 0, 'Mean': mu, f'{bounds[0]}%': lb, f'{bounds[1]}%': ub})
    for i, (mu, lb, ub) in enumerate(zip(delta, lbs, ubs)):
        reliability.append({'Param': param, 'Type': 'trt', 'Group': i+1, 'Mean': mu, f'{bounds[0]}%': lb, f'{bounds[1]}%': ub})
        
## Convert to DataFrame.
reliability = DataFrame(reliability)

## Format data.
cols = reliability.columns[np.in1d(reliability.dtypes, [np.float16, np.float32, np.float64])]
reliability[cols] = reliability[cols].round(6)

## Save data.
reliability.to_csv(os.path.join(ROOT_DIR, 'study02', 'stan_results', f'{stan_model}_reliability_comp.csv'), index=False)