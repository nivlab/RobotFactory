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
SURVEYS = []
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
    
    ## Define columns of interest.
    cols = ['Block','Trial','Valence','Action','Robot','Rune','Color','Correct',
            'Choice','RT','Accuracy','Sham','Outcome','TotalKeys']
        
    ## Limit to columns of interest.
    data = data[cols]
    
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
        Total = np.round(JSON[-1]['time_elapsed'] * 1e-3 / 60, 2)
    )
    
    ## Gather surveys.
    DEMO, = [dd for dd in JSON if dd['trial_type'] == 'survey-demo']
    DEBRIEF, = [dd for dd in JSON if dd['trial_type'] == 'survey-debrief']
    COMP = len([dd for dd in JSON if dd['trial_type'] == 'pit-comprehension'])
    
    ## Append surveys.
    dd.update(DEMO['responses']); dd['Demo-RT'] = DEMO['rt'] * 1e-3
    dd['Comp-Loops'] = COMP
    dd.update(DEBRIEF['responses']); dd['Debrief-RT'] = DEMO['rt'] * 1e-3
    
    ## Append.
    METADATA.append(dd)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Assemble survey data.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    ## Gather surveys.
    templates = [dd for dd in JSON if dd['trial_type'] == 'survey-template']
        
    ## Initialize dictionary.
    dd = dict(Subject=subject)
    
    for prefix in ['gad7','7up7down','bisbas']:
        
        ## Extract survey.
        survey, = [d for d in templates if d['survey']==prefix]
        
        ## Format prefix.
        if prefix == '7up7down': prefix = '7U7D'
        prefix = prefix.upper()
        
        ## Get RT.
        rt = np.copy(np.round(survey['rt'] * 1e-3, 3))
        
        ## Reformat responses.
        survey = {f'{prefix}-{k}': survey['responses'][k] for k in sorted(survey['responses'])}
    
        ## Update dictionary.
        dd.update(survey)
        dd[f'{prefix}-RT'] = rt

    ## Append.
    SURVEYS.append(dd)
    
## Concatenate data.
DATA = concat(DATA).sort_values(['Subject','Trial'])
SURVEYS = DataFrame(SURVEYS).sort_values(['Subject'])
METADATA = DataFrame(METADATA).sort_values(['Subject'])

## Save.
DATA.to_csv(os.path.join(DATA_DIR, 'data.csv'), index=False)
SURVEYS.to_csv(os.path.join(DATA_DIR, 'surveys.csv'), index=False)
METADATA.to_csv(os.path.join(DATA_DIR, 'metadata.csv'), index=False)