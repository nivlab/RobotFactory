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
    SURVEYS = []    

    for f in files:

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Load JSON file.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        ## Load file.
        subject = f.replace('.json','')

        with open(os.path.join(RAW_DIR, session, f), 'r') as f:
            JSON = json.load(f)
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Assemble survey data.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        ## Initialize dictionary.
        dd = dict(subject=subject, session=session[-1])

        ## Add affective slider.
        slider, = [dd for dd in JSON if dd['trial_type'] == 'affective-slider']
        dd['mood'] = slider['loc']
        
        ## Gather surveys.
        templates = [dd for dd in JSON if dd['trial_type'] == 'survey-template']

        for prefix in ['gad7', 'dass', 'bisbas']:

            ## Extract survey.
            survey = [d for d in templates if prefix in d.get('survey', d['trial_type'])]
            if survey: survey, = survey
            else: continue

            ## Update dictionary.
            dd[f'{prefix}_rt'] = np.copy(np.round(survey['rt'] * 1e-3, 3))
            dd[f'{prefix}_radio'] = len(survey['radio_events'])
            dd[f'{prefix}_key'] = len(survey['key_events'])
            dd[f'{prefix}_mouse'] = len(survey['mouse_events'])
            dd[f'{prefix}_ipi'] = np.round(np.median(np.diff(survey['radio_events']) * 1e-3), 3)
            dd[f'{prefix}_infreq'] = survey['infrequency']
            dd[f'{prefix}_sl'] = np.round(survey['straightlining'], 3)
            dd[f'{prefix}_zz'] = np.round(survey['zigzagging'], 3)

            ## Reformat responses.
            survey = {f'{prefix}_{k.lower()}': int(survey['responses'][k]) for k in sorted(survey['responses'])}

            ## BUG FIX.
            if prefix == "dass" and session == "day00":
                dd[f'{prefix}_infreq'] = [1,1,0.5,0][survey['dass_q08']]
            
            ## Update dictionary.
            dd.update(survey)
            
        ## Append.
        SURVEYS.append(dd)
    
    ## Concatenate data.
    SURVEYS = DataFrame(SURVEYS).sort_values(['subject','session'])

    ## Include summary data.
    score_ipi = lambda x: np.where(x < 0.2, 1, np.where(x < 0.5, 0.5, 0))
    SURVEYS.insert(2, 'infreq', SURVEYS.filter(regex='infreq').sum(axis=1))
    SURVEYS.insert(3, 'straightlining', (SURVEYS.filter(regex='sl') == 1.0).sum(axis=1))
    SURVEYS.insert(4, 'zigzagging', (SURVEYS.filter(regex='zz') == 1.0).sum(axis=1))
    SURVEYS.insert(5, 'ipi', (SURVEYS.filter(regex='ipi').apply(score_ipi)).sum(axis=1))

    ## Save.
    SURVEYS.to_csv(os.path.join(DATA_DIR, session, 'surveys.csv'), index=False)
