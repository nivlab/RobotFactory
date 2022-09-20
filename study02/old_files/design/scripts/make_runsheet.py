import os, sys
import numpy as np
from tqdm import tqdm

## Define seed.
try: seed = int(sys.argv[1])
except: seed = 47404
np.random.seed(seed)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define trial types.
robots = [0,1,2,3]    # GW, NGW, GAL, NGAL

## Define number of presentations.
seqlen = [8,10,12]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Generate trial order.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define useful functions.
def max_count(arr):
    return np.unique(arr, return_counts=True)[-1].max()

## Define metadata.
ncol = len(robots)
nrow = len(seqlen)
colsum = sum(seqlen)

## Initialize trial info.
B, A = [arr.flatten() for arr in np.meshgrid(seqlen, robots)]
C = np.arange(A.size)

order = np.arange(A.size)
for _ in tqdm(range(int(1e6))):
    
    ## Permutate order.
    np.random.shuffle(order)
    A = A[order]; B = B[order]; C = C[order]
      
    ## Check #1: All rows have no more than two of the same robot type.
    counts = np.apply_along_axis(max_count, 1, A.reshape(nrow,ncol))
    if np.any(counts >= 3): continue
        
    ## Check #2: All rows have diversity of valence.
    valence = A.reshape(nrow,ncol) // 2
    if np.any(np.all(valence == 1, axis=1) | np.all(valence == 0, axis=1)): continue
        
    ## Check #3: All rows have diversity of action.
    action = A.reshape(nrow,ncol) % 2
    if np.any(np.all(action == 1, axis=1) | np.all(action == 0, axis=1)): continue
        
    ## Check #4: All columns have equal sums.
    if not np.all(B.reshape(nrow,ncol).sum(axis=0) == colsum): continue
        
    ## Check #5: All rows have variable repetitions.
    counts = np.apply_along_axis(max_count, 1, B.reshape(nrow,ncol))
    if np.any(counts >= 3): continue
        
    break
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Fill in trials.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Reshape info.
A = A.reshape(nrow,ncol)
B = B.reshape(nrow,ncol)
C = C.reshape(nrow,ncol)

## Preallocate space.
robots = np.zeros((colsum, ncol), dtype=int)
stimuli = np.zeros_like(robots)

## Fill in trials.
for k in range(ncol):
    robots[:,k] = np.concatenate([np.tile(a,b) for a, b in zip(A[:,k],B[:,k])])
    stimuli[:,k] = np.concatenate([np.tile(c,b) for c, b in zip(C[:,k],B[:,k])])
    
## Randomize trial order.
order = np.arange(ncol)
for i in range(colsum):
    
    ## Permute order.
    np.random.shuffle(order)
    robots[i,:] = robots[i,order]
    stimuli[i,:] = stimuli[i,order]
    
## Re-order stimuli identitites.
shape = stimuli.shape
stimuli = stimuli.flatten()

dd = {}
for i, x in enumerate(stimuli):
    if not x in dd: dd[x] = len(dd)
    stimuli[i] = dd[x]

stimuli = stimuli.reshape(shape)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Format for JavaScript.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Dump to file.
with open('pit_runsheet_%s.txt' %seed, 'w') as f:
    
    ## Write latent order.
    f.write('Latent Order\n')
    f.write(np.array2string(A, separator=',') + '\n\n')
    
    ## Write robots.
    f.write('Robots\n')
    f.write(np.array2string(robots, separator=',') + '\n\n')
    
    ## Write stimuli.
    f.write('Stimuli\n')
    f.write(np.array2string(stimuli, separator=',') + '\n\n')