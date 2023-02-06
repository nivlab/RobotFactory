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

for session in ['s1','s2','s3','s4']:

    ## Locate files.
    files = sorted([f for f in os.listdir(os.path.join(RAW_DIR, session)) if f.endswith('json')])

    ## Preallocate space.
    SURVEYS = []

    for f in files:

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Load JSON file.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        ## Load file.
        subject, _ = f.replace('.json','').split('_')

        with open(os.path.join(RAW_DIR, session, f), 'r') as f:
            JSON = json.load(f)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Assemble survey data.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        ## Initialize dictionary.
        dd = dict(Subject=subject, Session=session[-1])

        ## Add affective slider.
        slider, = [dd for dd in JSON if dd['trial_type'] == 'affective-slider']
        dd['Slider'] = slider['loc']
        dd['Slider-RT'] = slider['time_elapsed'] * 1e-3

        ## Gather surveys.
        templates = [dd for dd in JSON if dd['trial_type'] == 'survey-template']

        for prefix in ['gad7','7up7down','bisbas']:

            ## Extract survey.
            survey = [d for d in templates if d['survey']==prefix]
            if survey: survey, = survey
            else: continue

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
    SURVEYS = DataFrame(SURVEYS).sort_values(['Subject','Session'])
    
    ## Format metadata.
    SURVEYS = SURVEYS.rename(columns={col: col.lower() for col in SURVEYS.columns})

    ## Save.
    SURVEYS.to_csv(os.path.join(DATA_DIR, session, 'surveys.csv'), index=False)
