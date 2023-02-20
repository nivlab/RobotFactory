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
    DATA = []    

    for f in files:

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Load JSON file.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        ## Load file.
        subject = f.replace('.json','')

        with open(os.path.join(RAW_DIR, session, f), 'r') as f:
            JSON = json.load(f)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Assemble behavioral data.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        ## Assemble behavioral data.
        data = DataFrame([dd for dd in JSON if dd['trial_type'] == 'pit-trial'])
        data = data.query('block > 0').reset_index(drop=True)
        
        ## Define columns of interest.
        cols = ['block','trial','stimulus','valence','action','robot','rune','rune_set','correct',
                'choice','rt','accuracy','sham','outcome','total_keys']

        ## Limit to columns of interest.
        data = data[cols]

        ## Reformat columns.
        data['block'] = data.block.astype(int)
        data['trial'] = data.trial.astype(int)
        data['stimulus'] = np.where(data.block == 1, 0, 12) + (data.stimulus.astype(int) + 1)
        data['correct'] = data.correct.replace({32: 1, -1:0})
        data['choice'] = data.choice.replace({32: 1, -1:0})
        data['rt'] = np.where(data.rt < 0, np.nan, data['rt'] * 1e-3).round(3)
        data['robot'] = data.robot.replace({1:'GW',2:'NGW',3:'GAL',4:'NGAL'})

        ## Define exposure.
        f = lambda x: np.arange(x.size)+1
        data.insert(2,'exposure',data.groupby('rune').trial.transform(f))

        ## Add subject.
        data.insert(0,'subject',subject)
        data.insert(1,'session',int(session[-1]))
        data.insert(3,'runsheet',0)
            
        ## Append.
        DATA.append(data)
    
    ## Concatenate data.
    DATA = concat(DATA).sort_values(['subject','session','trial'])

    ## Identify block runsheet.
    def block_version(df):
        session = df.name[1]; robots = df[:4].value_counts()
        if   (session == 1) and (robots['NGAL'] == 2): return '1a'
        elif (session == 1): return '1b'
        elif (session == 2) and (robots['GAL'] == 2): return '2b'
        elif (session == 2): return '2a'
        elif (session == 3) and (robots['NGW'] == 2): return '3b'
        else: return '3a'
    DATA['runsheet'] = DATA.groupby(['subject','session','block']).robot.transform(block_version)

    ## Format data.
    DATA = DATA.rename(columns={col: col.lower() for col in DATA.columns})
    DATA['valence'] = DATA.valence.replace({k: k.lower() for k in DATA.valence.unique()})
    DATA['action'] = DATA.action.replace({k: k.lower() for k in DATA.action.unique()})
    DATA['robot'] = DATA.robot.replace({k: k.lower() for k in DATA.robot.unique()})
    
    ## Standardize stimuli.
    DATA['x1'] = DATA.robot.replace({'gw': 1, 'ngw': 2, 'gal': 3, 'ngal': 4})
    DATA['x2'] = DATA.groupby(['subject','stimulus']).exposure.transform(np.max)
    DATA['stimulus'] = DATA.apply(lambda x: '%s_%0.2d_%0.2d' %(x.runsheet[-1], x.x1, x.x2), 1)
    DATA['stimulus'] = np.unique(DATA.stimulus, return_inverse=True)[-1] + 1
    DATA.drop(columns=['x1','x2'])
    
    ## Save.
    DATA.to_csv(os.path.join(DATA_DIR, session, 'pgng.csv'), index=False)
