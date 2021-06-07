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

## Define retest sessions.
sessions = ['day00', 'day03', 'day14']

## Preallocate space.
METADATA = []
SURVEYS = []
DATA = []

for i, session in enumerate(sessions):

    ## Locate files.
    sess_dir = os.path.join(RAW_DIR, session)
    files = sorted([f for f in os.listdir(sess_dir) if f.endswith('json')])

    for f in files:

        ## Load file.
        subject = f.replace('.json','')

        with open(os.path.join(sess_dir, f), 'r') as f:
            JSON = json.load(f)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Assemble behavioral data.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        ## Assemble behavioral data.
        data = DataFrame([dd for dd in JSON if dd['trial_type'] == 'pit-trial'])
        data = data.query('block > 0').reset_index(drop=True)

        ## Define columns of interest.
        cols = ['block','trial','valence','action','robot','stimulus','rune','rune_set','correct',
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
        data.insert(1,'session',i+1)
        DATA.append(data)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Assemble metadata.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        ## Initialize dictionary.
        dd = dict(
            subject = subject, 
            session = i+1,
            total = np.round(JSON[-1]['time_elapsed'] * 1e-3 / 60, 2),
            interactions = len(eval(JSON[-1]['interactions'])),
            practice_01 = len([dd for dd in JSON if dd.get('practice',None)==1]),
            practice_02 = len([dd for dd in JSON if dd.get('practice',None)==2]),
            practice_03 = len([dd for dd in JSON if dd.get('practice',None)==3]),
            practice_04 = len([dd for dd in JSON if dd.get('practice',None)==4]),
            comprehension = [dd for dd in JSON if dd['trial_type'] == 'pit-comprehension'][0]['num_errors']
        )

        ## Demographics
        DEMO = [dd for dd in JSON if dd['trial_type'] == 'survey-demo']
        if DEMO: dd.update(DEMO[0]['responses'])

        ## Debriefing
        DEBRIEF, = [dd for dd in JSON if dd['trial_type'] == 'survey-debrief']
        dd.update(DEBRIEF['responses']);

        ## Append.
        METADATA.append(dd)
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Assemble survey data.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        ## Initialize dictionary.
        dd = dict(subject=subject, session=i+1)

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
DATA = concat(DATA).sort_values(['subject','session','trial'])
SURVEYS = DataFrame(SURVEYS).sort_values(['subject','session'])
METADATA = DataFrame(METADATA).sort_values(['subject','session'])

## Include summary data.
score_ipi = lambda x: np.where(x < 0.2, 1, np.where(x < 0.5, 0.5, 0))
SURVEYS.insert(2, 'infreq', SURVEYS.filter(regex='infreq').sum(axis=1))
SURVEYS.insert(3, 'straightlining', (SURVEYS.filter(regex='sl') == 1.0).sum(axis=1))
SURVEYS.insert(4, 'zigzagging', (SURVEYS.filter(regex='zz') == 1.0).sum(axis=1))
SURVEYS.insert(5, 'ipi', (SURVEYS.filter(regex='ipi').apply(score_ipi)).sum(axis=1))

## Save.
DATA.to_csv(os.path.join(DATA_DIR, 'data.csv'), index=False)
SURVEYS.to_csv(os.path.join(DATA_DIR, 'surveys.csv'), index=False)
METADATA.to_csv(os.path.join(DATA_DIR, 'metadata.csv'), index=False)