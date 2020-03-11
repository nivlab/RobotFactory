import os, json
import numpy as np
from os.path import dirname
from pandas import DataFrame, concat
ROOT_DIR = dirname(dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DIR = os.path.join(ROOT_DIR, 'raw')

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
    data = data.query('Block > 0')

    ## Version testing.
    try: 
        
        ## Define columns of interest.
        cols = ['Block','Trial','Valence','Action','Robot','Rune','Correct',
                'Choice','RT','Accuracy','Sham','Outcome','TotalKeys']
        
        ## Limit to columns of interest.
        data = data[cols]
        
        ## Insert version ID.
        data.insert(0,'Version',2)
        
    except KeyError:
                
        ## Define columns of interest.
        cols = ['Block','Trial','Valence','Action','Correct','Choice',
                'RT','Accuracy','Sham','Outcome']
        
        ## Limit to columns of interest.
        data = data[cols]
        
        ## Insert version ID and missing columns.
        data.insert(0,'Version',1)
        data.insert(5,'Robot',np.nan)
        data.insert(6,'Rune',np.nan)
        data['TotalKeys'] = np.nan

    ## Reformat columns.
    data['Block'] = data['Block'].astype(int)
    data['Trial'] = data['Trial'].astype(int)
    data['Correct'] = data['Correct'].replace({32: 1, -1:0})
    data['Choice'] = data['Choice'].replace({32: 1, -1:0})
    data['RT'] = np.where(data['RT'] < 0, np.nan, data['RT'] * 1e-3).round(3)
    
    ## Insert subject ID. Append.
    data.insert(0,'Subject',subject)
    DATA.append(data)    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Assemble metadata.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    ## Gather surveys.
    DEMO, = [dd for dd in JSON if dd['trial_type'] == 'survey-demo']
    COMP, = [dd for dd in JSON if dd['trial_type'] == 'pit-comprehension']
    DEBRIEF, = [dd for dd in JSON if dd['trial_type'] == 'survey-debrief']
    
     ## Assemble dictionary.
    dd = dict(Subject = subject)
    dd.update(DEMO['demographics']); dd['Demo-RT'] = DEMO['rt'] / 1000.
    dd['Comp-Errors'] = COMP['errors']; dd['Comp-RT'] = COMP['rt'] / 1000.
    dd.update(DEBRIEF['debriefgraphics']); dd['Debrief-RT'] = DEMO['rt'] / 1000.
    
    ## Append.
    METADATA.append(dd)
    
## Concatenate data.
DATA = concat(DATA).sort_values(['Version','Subject','Trial'])
METADATA = DataFrame(METADATA, columns=dd.keys()).sort_values('Subject')
METADATA = METADATA.merge(DATA[['Subject','Version']])

## Save.
DATA.to_csv(os.path.join(DATA_DIR, 'data.csv'), index=False)
METADATA.to_csv(os.path.join(DATA_DIR, 'metadata.csv'), index=False)