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

for session in ['s1','s2','s3']:

    ## Locate files.
    files = sorted([f for f in os.listdir(os.path.join(RAW_DIR, session)) if f.endswith('json')])
    
    ## Preallocate space.
    METADATA = []    
    DEMO = []
    
    for f in files:

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Load JSON file.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        ## Load file.
        subject = f.replace('.json','')

        with open(os.path.join(RAW_DIR, session, f), 'r') as f:
            JSON = json.load(f)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Assemble metadata.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        ## Initialize dictionary.
        dd = dict(
            subject = subject, 
            session = session[-1],
            total = np.round(JSON[-1]['time_elapsed'] * 1e-3 / 60, 2),
            interactions = len(eval(JSON[-1]['interactions'])),
            practice_01 = len([dd for dd in JSON if dd.get('practice',None)==1]),
            practice_02 = len([dd for dd in JSON if dd.get('practice',None)==2]),
            practice_03 = len([dd for dd in JSON if dd.get('practice',None)==3]),
            practice_04 = len([dd for dd in JSON if dd.get('practice',None)==4]),
            comprehension = [dd for dd in JSON if dd['trial_type'] == 'pit-comprehension'][0]['num_errors']
        )

        ## Demographics
        try:
            demo, = [dd for dd in JSON if dd['trial_type'] == 'survey-demo']
            tmp = dict(subject=subject, session=session)
            tmp.update(demo['responses'])
            DEMO.append(tmp)
        except:
            pass

        ## Debriefing
        DEBRIEF, = [dd for dd in JSON if dd['trial_type'] == 'survey-debrief']
        dd.update(DEBRIEF['responses']);

        ## Append.
        METADATA.append(dd)
    
    ## Concatenate data.
    METADATA = DataFrame(METADATA).sort_values(['subject','session'])
    DEMO = DataFrame(DEMO)
    
    ## Format metadata.
    METADATA = METADATA.rename(columns={col: col.lower() for col in METADATA.columns})
    
    ## Format demographics data.
    if len(DEMO):
        DEMO = DEMO.sort_values(['subject','session'])
        DEMO = DEMO.rename(columns={col: col.lower() for col in DEMO.columns})
        DEMO = DEMO.rename(columns={'gender-categorical': 'gender', 'language': 'english'})
        DEMO = DEMO.replace({'Male': 'Man', 'Female': 'Woman'})
        
    ## Save.
    METADATA.to_csv(os.path.join(DATA_DIR, session, 'metadata.csv'), index=False)
    if len(DEMO): DEMO.to_csv(os.path.join(DATA_DIR, session, 'demographics.csv'), index=False)
