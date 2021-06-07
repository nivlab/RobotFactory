import os, json
import numpy as np
from os.path import dirname
from pandas import DataFrame, concat
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'v0.1')
RAW_DIR = os.path.join(ROOT_DIR, 'raw', 'v0.1')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Main loop.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Locate files.
files = sorted([f for f in os.listdir(RAW_DIR) if f.endswith('json')])

## Preallocate space.
METADATA = []
DATA = []

for f in files:
    
    ## Load file.
    subject = f.replace('.json','')
    
    with open(os.path.join(RAW_DIR, f), 'r') as f:
        JSON = json.load(f)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Assemble behavioral data.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    ## Assemble behavioral data.
    data = DataFrame([dd for dd in JSON if dd['trial_type'] == 'pit-trial'])
    data = data.query('block > 0').reset_index(drop=True)
    
    ## Define columns of interest.
    cols = ['block','trial','valence','action','robot','rune','correct',
            'choice','rt','accuracy','sham','outcome','total_keys']
        
    ## Limit to columns of interest.
    data = data[cols]
    
    ## Reformat columns.
    data['block'] = data['block'].astype(int)
    data['trial'] = data['trial'].astype(int)
    data['correct'] = data['correct'].replace({32: 1, -1:0})
    data['choice'] = data['choice'].replace({32: 1, -1:0})
    data['rt'] = np.where(data['rt'] < 0, np.nan, data['rt'] * 1e-3).round(3)
    data['robot'] = data['robot'].replace({1:'GW',2:'NGW',3:'GAL',4:'NGAL'})
    
    ## Define exposure.
    f = lambda x: np.arange(x.size)+1
    data.insert(2,'exposure',data.groupby('rune').trial.transform(f))
    
    ## Add subject. Append.
    data.insert(0,'subject',subject)
    DATA.append(data)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Assemble metadata.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    ## Initialize dictionary.
    dd = dict(
        subject = subject, 
        total = np.round(JSON[-1]['time_elapsed'] * 1e-3 / 60, 2),
        interactions = len(eval(JSON[-1]['interactions'])),
        instructions = len([dd for dd in JSON if dd['trial_type'] == 'pit-comprehension'])
    )
    
    ## Demographics
    DEMO, = [dd for dd in JSON if dd['trial_type'] == 'survey-demo']
    dd.update(DEMO['responses'])

    ## Debriefing
    DEBRIEF, = [dd for dd in JSON if dd['trial_type'] == 'survey-debrief']
    dd.update(DEBRIEF['responses']);
    
    ## Append.
    METADATA.append(dd)
    
## Concatenate data.
DATA = concat(DATA).sort_values(['subject','trial'])
METADATA = DataFrame(METADATA).sort_values(['subject'])

## Save.
DATA.to_csv(os.path.join(DATA_DIR, 'data.csv'), index=False)
METADATA.to_csv(os.path.join(DATA_DIR, 'metadata.csv'), index=False)