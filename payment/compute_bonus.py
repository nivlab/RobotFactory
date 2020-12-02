import os, json
import numpy as np
from os.path import dirname
from pandas import DataFrame, concat
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
METADATA_DIR = os.path.join(ROOT_DIR, 'metadata')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Metadata directory.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Locate files.
files = sorted([f for f in os.listdir(METADATA_DIR) if f.startswith('A')])

METADATA = []
for f in files:

    ## Load file.
    worker = f
    with open(os.path.join(METADATA_DIR, f), 'r') as f:
        for line in f.readlines():
           if 'subId' in line:
               METADATA.append( dict(workerId=worker, subId=line.strip().split('\t')[-1]) )

## Convert to DataFrame.
METADATA = DataFrame(METADATA)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Data directory.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Locate files.
files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.json')])

DATA = []
for f in files:

    ## Load file.
    subject = f.replace('.json','')
    with open(os.path.join(DATA_DIR, f), 'r') as f:
        JSON = json.load(f)

    ## Locate learning trials.
    data = DataFrame([dd for dd in JSON if dd['trial_type'] == 'pit-trial'])
    data = data.query('block > 0')

    ## Compute accuracy.
    accuracy = data.accuracy.mean()

    ## Store.
    DATA.append( dict(subId=subject, accuracy=accuracy) )

## Convert to DataFrame.
DATA = DataFrame(DATA)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Compute bonus.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define maximum bonus.
completion_bonus = 0.00
max_bonus = 1.50

## Merge DataFrames.
BONUS = METADATA.merge(DATA, on='subId', how='inner')
BONUS['bonus'] = np.round(BONUS['accuracy'] * max_bonus + completion_bonus, 2)

## Save.
BONUS.to_csv('bonus.csv', index=False, header=False, columns=('workerId','bonus'))
print(BONUS.bonus.sum(), bonus.bonus.sum() * 1.2)
