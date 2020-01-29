import os
import numpy as np
from pandas import DataFrame, concat, read_csv
from scipy.io import loadmat
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def preprocess_2016albrecht(data_dir = '2016albrecht'):
    """Load and prepare data from Albrecht et al. (2016)."""
    
    ## Load data.
    data = read_csv(os.path.join(data_dir,'dftr.csv'))
    
    ## Restrict to healthy controls.
    data = data.query('group=="HC"')

    ## Restrict and rename columns.
    data = data[['sidx','trial','IdealOutcome','TrialType','ttOut',
                 'Respond','Target.RT','Accuracy','MoneyEarned']]
    data.columns = ('Subject','Trial','Valence','Action','Cue','Choice','RT','Accuracy','Outcome')

    ## Update subject info.
    data['Subject'] = np.unique(data.Subject, return_inverse=True)[-1] + 1

    ## Update condition info.
    data['Valence'] = data.Valence.replace({'Win':'Win', 'Avoid-loss':'Lose'})
    data['Action']  = data.Action.replace({'Go':'Go', 'No-go':'No-Go'})
    data['Cue'] = data.Cue.replace({'Go.Win':1, 'Go.Avoid-loss':2, 'No-go.Win':3, 'No-go.Avoid-loss':4})

    ## Update trial info.
    tally = lambda arr: np.arange(arr.size) + 1
    data['Block'] = 1
    data['Exposure'] = data.groupby(['Subject','Cue']).Trial.transform(tally)

    ## Update response info.
    data['Choice'] = data['Choice'].astype(int)
    data['RT'] = data.RT.replace({0:np.nan}) / 1000.
    
    ## Update outcome info.
    delta = data.groupby('Subject').Outcome.diff()
    data['Outcome'] = np.where(np.isnan(delta), data.Outcome, delta)
    data['Outcome'] = np.sign(data.Outcome).astype(int)

    data['Study'] = data_dir
    return data


def preprocess_2017mkrtchian(data_dir = '2017mkrtchian'):
    """Load and prepare data from Mkrtchian et al. (2017).
    
    Notes
    -----
    - The task involves a target detection sub-task, wherein participants must identify
      and indicate the spatial location of a visual target. On a rare minority of trials,
      this results in erroneous responses on Go trials (e.g. participant correctly responds
      but incorrectly identifies the correct location of the target). Because on these 
      trials the participant has successfuly learned the Go-rule, but has made a simple
      motor error (press wrong side button), we set these trials to NaNs. This should
      affect the overwhelming minority of participants in the sample.
    
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Load and prepare data.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## Locate files.
    files = sorted([f for f in os.listdir(data_dir) if f.startswith('LOGS')])

    ## Main loop.
    data = []
    for i, f in enumerate(files):

        ## Load data.
        df = read_csv(os.path.join(data_dir,f), sep=' ')

        ## Rename columns.
        df.columns = ('Subject','Trial','Condition','Cue',
                      'OutcomeCorrect','OutcomeIncorrect','OutcomeNoPress',
                      'Outcome','','Choice','Accuracy','RT','')

        ## Update subject info.
        df['Subject'] = int(''.join([s for s in f if s.isnumeric()]))

        ## Update condition info.
        df['Condition'] = np.where(df.Condition==1, 'Threat', 'Control')
        df['Valence'] = df.Cue.replace({1:'Win', 2:'Lose', 3:'Win', 4:'Lose'})
        df['Action'] = df.Cue.replace({1:'Go', 2:'Go', 3:'No-Go', 4:'No-Go'})

        ## Update trial info.
        tally = lambda arr: np.arange(arr.size) + 1
        df['Block'] = 1
        df['Trial'] = df.groupby('Condition').Trial.transform(tally)
        df['Exposure'] = df.groupby(['Condition','Cue']).Trial.transform(tally)
        
        ## Filter error trials.
        ix = df.query('Action=="Go" and RT > 0 and Accuracy==0').index
        df.loc[ix,['Choice','Accuracy','RT','Outcome']] = np.nan
        df['Choice'] = df.Choice.replace({0:0, 1:1, 2:1})
        
        ## Restrict to columns of interest.
        df = df[['Subject','Condition','Block','Trial','Exposure','Cue','Valence','Action',
                 'Choice','Accuracy','RT','Outcome']]

        ## Append.
        data.append(df)

    ## Concatenate data.    
    data = concat(data)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Load and prepare metadata.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    ## Load metadata.
    metadata = read_csv(os.path.join(data_dir,'STAIData.csv'))

    ## Update diagnostic category.
    metadata['Diagnosis'] = metadata.Diagnosis.replace({'HC':np.nan,'patient':'Anxious'})

    ## Update subject info.
    to_numeric = lambda label: int(''.join([s for s in label if s.isnumeric()]))
    metadata['Subject'] = metadata.Subject.apply(to_numeric)

    ## Merge with data.
    data = data.merge(metadata[['Diagnosis','Subject']], on='Subject')
    
    ## Update subject info.
    data['Subject'] = np.unique(data.Subject, return_inverse=True)[-1] + 1
    data['Study'] = data_dir
    
    return data


def preprocess_2018millner(data_dir = '2018millner'):
    """Load and prepare data from Millner et al. (2018)."""
    
    ## Load data.
    data = read_csv(os.path.join(data_dir,'data.csv'))

    ## Rename columns.
    data.columns = ('Trial','Valence','Action','Choice','Outcome','Accuracy',
                    'RT','Subject','','')

    ## Update subject info.
    data['Subject'] = np.unique(data.Subject, return_inverse=True)[-1] + 1
    
    ## Update condition info.
    data['Valence'] = data.Valence.replace(dict(Avoid='Win',Escape='Lose'))
    data['Action'] = data.Action.replace(dict(Go='Go',NoGo='No-Go'))
    data['Cue'] = data[['Valence','Action']].apply(lambda x: f'{x.values[0]}-{x.values[1]}', 1)
    data['Cue'] = data.Cue.replace({'Win-Go':1, 'Win-No-Go':2, 'Lose-Go':3, 'Lose-No-Go':4})

    ## Update trial info.
    tally = lambda arr: np.arange(arr.size) + 1
    data['Block'] = 1
    data['Trial'] += 1
    data['Exposure'] = data.groupby(['Subject','Cue']).Trial.transform(tally)
    
    ## Restrict to columns of interest.
    data = data[['Subject','Block','Trial','Exposure','Cue','Valence','Action',
                 'Choice','Accuracy','RT','Outcome']]
    data['Study'] = data_dir
    
    return data


def preprocess_2018moutoussis(data_dir = '2018moutoussis'):
    """Load and prepare data from Moutoussis et al. (2018)."""
    
    ## Locate files.
    files = sorted([f for f in os.listdir('2018moutoussis') if f.endswith('mat')])

    ## Main loop.
    data = []
    for f in files:

        ## Gather metadata.
        subject = f.split('_')[0]
        session = 'Retest' if '_mk2GNG1_' in f else 'Control'

        ## Load mat file.
        mat = loadmat(os.path.join('2018moutoussis',f))

        ## Convert to DataFrame.
        df = DataFrame(mat['LearnVerData'], columns=np.arange(17)+1)[[2,12,17]]
        df.columns = ['Cue','RT','Outcome']

        ## Insert metadata.
        df.insert(0, 'Subject', subject)
        df.insert(1, 'Condition', session)
        df.insert(2, 'Block', 1)
        df.insert(3, 'Trial', np.arange(df.shape[0])+1)

        ## Append.
        data.append(df)

    ## Concatenate data.
    data = concat(data)
    data.insert(0, 'Study', '2018moutoussis')

    ## Update cue information.
    data['Cue'] = data.Cue.astype(int)

    ## Insert valence information.
    f = lambda x: np.where(np.any(x > 0), 'Win', 'Lose')
    data.insert(5, 'Valence', data.groupby('Cue').Outcome.transform(f))

    ## Insert action information.
    data.insert(6, 'Action', data.Cue.replace({1:'Go', 2:'Go', 3:'No-Go', 4:'No-Go'}))

    ## Insert exposure information.
    tally = lambda arr: np.arange(arr.size) + 1
    data.insert(8, 'Exposure', data.groupby(['Subject','Condition','Cue']).Trial.transform(tally))

    ## Update RT information.
    data['RT'] = np.where(data.RT > 0, data.RT / 1000., np.nan)

    ## Insert choice information.
    data.insert(9, 'Choice', data.RT.notnull().astype(int))

    ## Insert accuracy.
    data.insert(11, 'Accuracy', ((data.Action=='Go') == (data.Choice)).astype(int))
    
    return data

def preprocess_2018swart(data_dir = '2018swart'):
    """Load and prepare data from Swart et al. (2018).
    
    Notes
    -----
    - Two participants had a few (1-2) missing outcomes. These were set 
      to the most likely outcome.
    - 43 trials had errors in keypress coding, i.e. not in [0, 97, 101]. The 
      majority of these trials are too slow responses (>1300ms). These trials 
      have their response values set to NaN. 
    """
        
    ## Locate files.
    files = sorted([f for f in os.listdir(data_dir) if f.endswith('mat')])

    ## Main loop.
    data = []
    for i, f in enumerate(files):

        ## Load mat file.
        mat = loadmat(os.path.join(data_dir, f), squeeze_me=True)

        ## Extract cue information.
        par, _, seq, _ = mat['prep'].tolist()    # params, dir, sequence, timing
        seq, _ = seq.tolist()
        stim, feedback, resp, iti = seq.tolist()

        cue = np.concatenate(stim)
        cue_id = par.tolist()[7][cue - 1]

        ## Extract behavior. 
        results = mat['results']
        session_1, session_2 = [sess.tolist() for sess in results.tolist()[1].tolist()]
        rt = np.concatenate([session_1[0], session_2[0]])
        accuracy = np.concatenate([session_1[1], session_2[1]])
        response = np.concatenate([session_1[2], session_2[2]])
        outcome = np.concatenate([session_1[3], session_2[3]])

        ## Convert to DataFrame
        df = DataFrame(dict(Cue=cue, X=cue_id, RT=rt, Accuracy=accuracy, 
                            Choice=response, Outcome=outcome))

        ## Update subject info.
        df['Subject'] = i + 1

        ## Update condition info.
        df['Valence'] = df.X.apply(lambda x: 'Win' if 'win' in x else 'Lose')
        df['Action'] = df.X.apply(lambda x: 'No-Go' if 'NoGo' in x else 'Go')

         ## Update trial info.
        tally = lambda arr: np.arange(arr.size) + 1
        df['Block'] = np.repeat([1,2],320)
        df['Trial'] = np.concatenate([np.arange(320),np.arange(320)])+1
        df['Exposure'] = df.groupby(['Block','Cue']).Trial.transform(tally)

        ## Update response info.
        df['Choice'] = df.Choice.replace({0:0, 97:1, 101:2})
        
        ## Filter "error" trials. 
        df.loc[np.in1d(df.Choice, [65,69,99]), ('Choice','RT','Accuracy','Outcome')] = np.nan
        
        ## Update outcome info.
        f = lambda x: x['X']-(1-x['Accuracy']) if np.isnan(x['Outcome']) else x['Outcome']
        df['X'] = df.Valence.replace({'Win':1,'Lose':0})
        df['Outcome'] = df.apply(f, axis=1)
        
        ## Append.
        data.append(df)
        
    ## Concatenate data.    
    data = concat(data)
    
    data['Study'] = data_dir
    return data


def preprocess_2019csifcsal(data_dir = '2019csifcsal'):
    """Load and prepare data from Csifcsal et al. (2019)."""

    ## Locate files.
    files = sorted([f for f in os.listdir(data_dir) if f.endswith('csv')])

    ## Main loop.
    data = []
    i = 0
    for f in files:

        ## Load data.
        df = read_csv(os.path.join(data_dir,f), comment="#")

        ## Skip yoked condition.
        if df.condition.isin(['yoked']).any(): continue
        i += 1

        ## Restrict and rename columns.
        df = df[['subj','session_index','trial','cardnumber','trial_type',
                 'reward_type','response','RT','RT_in_frames']]
        df.columns = ('Subject','Block','Trial','Cue','Action','Valence','Choice','RT','Outcome')

        ## Update subject info.
        df['Subject'] = i

        ## Update condition info.
        df['Valence'] = df.Valence.replace({'win':'Win', 'avoid':'Lose'})
        df['Action'] = df.Action.replace({'go':'Go', 'nogo':'No-Go'})

        ## Update trial info.
        tally = lambda arr: np.arange(arr.size) + 1
        df['Trial'] += 1
        df['Exposure'] = df.groupby(['Block','Cue']).Trial.transform(tally)

        ## Update response info.
        df['RT'] = df.RT.replace({-1:np.nan})
        df['Accuracy'] = np.logical_or((df.Action=="Go")&(df.Choice==1),
                                       (df.Action=="No-Go")&(df.Choice==0)).astype(int)
        
        ## Update outcome info.
        df['Outcome'] /= 10

        ## Append.
        data.append(df)

    ## Concatenate data.    
    data = concat(data)

    data['Study'] = data_dir
    return data


def preprocess_201Xcsifcsal(data_dir = '202Xcsifcsal'):
    """Load and prepare data from Csifcsal et al. (unpublished)."""

    ## Locate files.
    files = sorted([f for f in os.listdir(data_dir) if f.endswith('csv')])

    ## Main loop.
    data = []
    i = 0
    for f in files:

        ## Load data.
        df = read_csv(os.path.join(data_dir,f), comment="#")

        ## Skip yoked condition.
        if df.condition.isin(['yoked']).any(): continue
        elif df.shape[0] < 160: continue
        i += 1

        ## Restrict and rename columns.
        df = df[['subj','session_index','trial','cardnumber','trial_type',
                 'reward_type','response','RT','RT_in_frames']]
        df.columns = ('Subject','Block','Trial','Cue','Action','Valence','Choice','RT','Outcome')

        ## Update subject info.
        df['Subject'] = i
        df['Condition'] = 'tDCS'

        ## Update condition info.
        df['Valence'] = df.Valence.replace({'win':'Win', 'avoid':'Lose'})
        df['Action'] = df.Action.replace({'go':'Go', 'nogo':'No-Go'})

        ## Update trial info.
        tally = lambda arr: np.arange(arr.size) + 1
        df['Trial'] += 1
        df['Exposure'] = df.groupby(['Block','Cue']).Trial.transform(tally)

        ## Update response info.
        df['RT'] = df.RT.replace({-1:np.nan})
        df['Accuracy'] = np.logical_or((df.Action=="Go")&(df.Choice==1),
                                       (df.Action=="No-Go")&(df.Choice==0)).astype(int)
        
        ## Update outcome info.
        df['Outcome'] /= 10

        ## Append.
        data.append(df)

    ## Concatenate data.    
    data = concat(data)

    data['Study'] = data_dir
    return data


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Assemble data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load and concatenate data.
data = concat([
    preprocess_2016albrecht(),
    preprocess_2017mkrtchian(), 
    preprocess_2018millner(), 
    preprocess_2018moutoussis(), 
    preprocess_2018swart(), 
    preprocess_2019csifcsal(),
    preprocess_201Xcsifcsal()
], sort=False)

## Reorder columns.
data = data[['Study','Subject','Diagnosis','Condition','Block','Trial','Valence','Action','Cue',
             'Exposure','Choice','RT','Accuracy','Outcome']]

## Re-sort rows.
data = data.sort_values(['Study','Subject','Condition','Block','Trial'])

## Format data.
data['Diagnosis'] = data.Diagnosis.fillna('Healthy')
data['Condition'] = data.Condition.fillna('Control')
data['RT'] = data.RT.round(3)

## Save data.
data.to_csv(os.path.join(os.path.dirname(ROOT_DIR),'data.csv'), index=False)