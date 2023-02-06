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
    DATA = []

    for f in files:

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        ### Load JSON file.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        ## Load file.
        subject, _ = f.replace('.json','').split('_')

        with open(os.path.join(RAW_DIR, session, f), 'r') as f:
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
        data.insert(2, 'Exposure', data.groupby('Rune').Trial.transform(lambda x: np.arange(x.size) + 1))

        ## Define stimulus.
        data.insert(3, 'Stimulus', data.Rune.replace({k:i+1 for i, k in enumerate(data.Rune.unique())}))
        
        ## Insert subject ID. Append.
        data.insert(0, 'Subject', subject)
        data.insert(1, 'Session', int(session[-1]))
        DATA.append(data)    

    ## Concatenate data.
    DATA = concat(DATA).sort_values(['Subject','Session','Trial'])
    
    ## Format data.
    DATA = DATA.rename(columns={col: col.lower() for col in DATA.columns})
    DATA['valence'] = DATA.valence.replace({k: k.lower() for k in DATA.valence.unique()})
    DATA['action'] = DATA.action.replace({k: k.lower() for k in DATA.action.unique()})
    DATA['robot'] = DATA.robot.replace({k: k.lower() for k in DATA.robot.unique()})
    
    ## Save.
    DATA.to_csv(os.path.join(DATA_DIR, session, 'pgng.csv'), index=False)
