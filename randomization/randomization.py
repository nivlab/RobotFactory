import numpy as np
from pandas import DataFrame
from itertools import permutations
np.random.seed(47404)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
n_block = 2
n_stim  = 4
n_tri_per_stim = 20

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define trial order.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define all possible sequences.
seqs = np.array(list(permutations(range(n_stim),n_stim)))

## Randomly select sequences.
ix = np.random.choice(np.arange(seqs.shape[0]), n_tri_per_stim * n_block, replace=True)

## Define order.
order = np.concatenate(seqs[ix])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define task details.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Initialize DataFrame.
data = np.column_stack([np.arange(order.size)+1, order+1])
data = DataFrame(data, columns=('Trial','Robot'))

## Add info.
data['Block'] = np.arange(order.size) // (order.size // n_block) + 1
data['Valence'] = np.where(data['Robot'] <= 2, 'Win', 'Lose')
data['Action'] = np.where(data['Robot'] % 2, 'Go', 'No-Go')
data['Correct'] = np.where(data['Action']=='Go',32,-1)
data['Robot'] = data['Robot'] + (4 * (data['Block']-1))

## Add sham trials.
def simulate_outcomes(x=[0,0,0,0,1], n=4):
    outcomes = []
    for _ in range(n):
        np.random.shuffle(x)
        outcomes.append(x.copy())
    return np.concatenate(outcomes)

data['Sham'] = data.groupby('Robot').Block.transform(lambda x: simulate_outcomes())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Save.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Reorganize columns.
data = data[['Block','Trial','Valence','Action','Correct','Sham']]

## Save.
data.to_csv('pit.csv', index=False)
print(data.to_json(orient='records'))
