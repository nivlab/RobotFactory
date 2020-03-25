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
    
    ## Check if Version 1.
    if data.shape[-1] == 14:
        
        ## Define columns of interest.
        cols = ['Block','Trial','Valence','Action','Correct','Choice',
                'RT','Accuracy','Sham','Outcome']
        
        ## Limit to columns of interest.
        data = data[cols]
        
        ## Insert version ID and missing columns.
        data.insert(0,'Version',1)
        
    elif data.shape[-1] == 18:
        
        ## Define columns of interest.
        cols = ['Block','Trial','Valence','Action','Robot','Rune','Correct',
                'Choice','RT','Accuracy','Sham','Outcome','TotalKeys']
        
        ## Limit to columns of interest.
        data = data[cols]
        
        ## Insert version ID and missing columns.
        data.insert(0,'Version',2)
        
    elif data.shape[-1] == 19:
        
        ## Define columns of interest.
        cols = ['Block','Trial','Valence','Action','Robot','Rune','Color','Correct',
                'Choice','RT','Accuracy','Sham','Outcome','TotalKeys']
        
        ## Limit to columns of interest.
        data = data[cols]
        
        ## Insert version ID and missing columns.
        data.insert(0,'Version',3)
        
    else:
        
        raise ValueError(f'Not sure which version this {subject} is.')
        
    ## Reformat columns.
    data['Block'] = data['Block'].astype(int)
    data['Trial'] = data['Trial'].astype(int)
    data['Correct'] = data['Correct'].replace({32: 1, -1:0})
    data['Choice'] = data['Choice'].replace({32: 1, -1:0})
    data['RT'] = np.where(data['RT'] < 0, np.nan, data['RT'] * 1e-3).round(3)
    
    ## Define robot identities.
    data.loc[np.logical_and(data.Valence=='Win',data.Action=='Go'),'Robot'] = 'GW'
    data.loc[np.logical_and(data.Valence=='Win',data.Action=='No-Go'),'Robot'] = 'NGW'
    data.loc[np.logical_and(data.Valence=='Lose',data.Action=='Go'),'Robot'] = 'GAL'
    data.loc[np.logical_and(data.Valence=='Lose',data.Action=='No-Go'),'Robot'] = 'NGAL'

    ## Define exposure.
    f = lambda x: np.arange(x.size)+1
    data.insert(3,'Exposure',data.groupby('Robot').Trial.transform(f))
    
    ## Insert subject ID. Append.
    data.insert(0,'Subject',subject)
    DATA.append(data)    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Assemble metadata.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    ## Initialize dictionary.
    dd = dict(
        Subject = subject, 
        Version = data.Version.unique()[0],
        Minutes = np.round(JSON[-1]['time_elapsed'] * 1e-3 / 60, 2)
    )
    
    ## Gather surveys.
    DEMO, = [dd for dd in JSON if dd['trial_type'] == 'survey-demo']
    COMP, = [dd for dd in JSON if dd['trial_type'] == 'pit-comprehension']
    DEBRIEF, = [dd for dd in JSON if dd['trial_type'] == 'survey-debrief']
    
    ## Append surveys.
    dd.update(DEMO['demographics']); dd['Demo-RT'] = DEMO['rt'] * 1e-3
    dd['Comp-Errors'] = COMP['errors']; dd['Comp-RT'] = COMP['rt'] * 1e-3
    dd.update(DEBRIEF['debriefgraphics']); dd['Debrief-RT'] = DEMO['rt'] * 1e-3
    
    ## Append.
    METADATA.append(dd)
    
## Concatenate data.
DATA = concat(DATA, sort=False).sort_values(['Version','Subject','Trial'])
METADATA = DataFrame(METADATA, columns=dd.keys()).sort_values(['Version','Subject'])

## Save.
DATA.to_csv(os.path.join(DATA_DIR, 'data.csv'), index=False)
METADATA.to_csv(os.path.join(DATA_DIR, 'metadata.csv'), index=False)