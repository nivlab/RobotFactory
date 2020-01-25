import os
import numpy as np
from pandas import DataFrame, concat, read_csv
from scipy.io import loadmat

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
    data = data[['sidx','group','trial','IdealOutcome','TrialType','ttOut',
                 'Respond','Target.RT','Accuracy','MoneyEarned']]
    data.columns = ('Subject','Diagnosis','Trial','Valence','Action','Cue','Choice','RT','Accuracy','Outcome')

    ## Update subject.
    data['Subject'] = np.unique(data.Subject, return_inverse=True)[-1] + 1

    ## Update condition info.
    data['Valence'] = data.Valence.replace({'Win':'Positive', 'Avoid-loss':'Negative'})
    data['Action']  = data.Action.replace({'Go':'Go', 'No-go':'No-Go'})
    data['Cue'] = data.Cue.replace({'Go.Win':1, 'Go.Avoid-loss':2, 'No-go.Win':3, 'No-go.Avoid-loss':4})

    ## Update trial info.
    tally = lambda arr: np.arange(arr.size) + 1
    data['Exposure'] = data.groupby(['Subject','Cue']).Trial.transform(tally)

    ## Update response info.
    data['Choice'] = data['Choice'].astype(int)
    data['RT'] = data.RT.replace({0:np.nan}) / 1000.

    data['Study'] = data_dir
    return data


def preprocess_2017mkrtchian(data_dir = '2017mkrtchian'):
    """Load and prepare data from Mkrtchian et al. (2017)."""

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

        ## Update subject.
        df['Subject'] = i + 1

        ## Update condition info.
        df['Condition'] = np.where(df.Condition==1, 'Threat', 'Safe')
        df['Valence'] = df.Cue.replace({1:'Positive', 2:'Negative', 3:'Positive', 4:'Negative'})
        df['Action'] = df.Cue.replace({1:'Go', 2:'Go', 3:'No-Go', 4:'No-Go'})

        ## Update trial info.
        tally = lambda arr: np.arange(arr.size) + 1
        df['Trial'] = df.groupby('Condition').Trial.transform(tally)
        df['Exposure'] = df.groupby(['Condition','Cue']).Trial.transform(tally)

        ## Restrict to columns of interest.
        df = df[['Subject','Condition','Trial','Exposure','Cue','Valence','Action',
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
    metadata['Diagnosis'] = metadata.Diagnosis.replace({'HC':'HC','patient':'Anx'})

    ## Update subject info.
    to_numeric = lambda label: int(''.join([s for s in label if s.isnumeric()]))
    metadata['Subject'] = metadata.Subject.apply(to_numeric)

    ## Merge with data.
    data = data.merge(metadata[['Diagnosis','Subject']], on='Subject')
    data['Study'] = data_dir
    
    return data


def preprocess_2018millner(data_dir = '2018millner'):
    """Load and prepare data from Millner et al. (2018)."""
    
    ## Load data.
    data = read_csv(os.path.join(data_dir,'data.csv'))

    ## Rename columns.
    data.columns = ('Trial','Valence','Action','Choice','Outcome','Accuracy',
                    'RT','Subject','','')

    ## Update subject.
    data['Subject'] = np.unique(data.Subject, return_inverse=True)[-1] + 1
    data['Diagnosis'] = 'HC'
    
    ## Update condition info.
    data['Valence'] = data.Valence.replace(dict(Avoid='Positive',Escape='Negative'))
    data['Action'] = data.Action.replace(dict(Go='Go',NoGo='No-Go'))
    data['Cue'] = data[['Valence','Action']].apply(lambda x: f'{x.values[0]}-{x.values[1]}', 1)
    data['Cue'] = data.Cue.replace({'Positive-Go':1, 'Positive-No-Go':2, 'Negative-Go':3, 'Negative-No-Go':4})

    ## Update trial info.
    tally = lambda arr: np.arange(arr.size) + 1
    data['Trial'] += 1
    data['Exposure'] = data.groupby(['Subject','Cue']).Trial.transform(tally)

    ## Restrict to columns of interest.
    data = data[['Subject','Diagnosis','Trial','Exposure','Cue','Valence','Action',
                 'Choice','Accuracy','RT','Outcome']]
    data['Study'] = data_dir
    
    return data


def preprocess_2018swart(data_dir = '2018swart'):
    
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
        df['Diagnosis'] = 'HC'

        ## Update condition info.
        df['Valence'] = df.X.apply(lambda x: 'Positive' if 'win' in x else 'Negative')
        df['Action'] = df.X.apply(lambda x: 'No-Go' if 'NoGo' in x else 'Go')

         ## Update trial info.
        tally = lambda arr: np.arange(arr.size) + 1
        df['Trial'] = np.concatenate([np.arange(320),np.arange(320)])+1
        df['Condition'] = np.repeat([1,2],320)
        df['Exposure'] = df.groupby(['Condition','Cue']).Trial.transform(tally)

        ## Update response info.
        df['Choice'] = df.Choice.replace({0:0, 97:1, 101:2})
        
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
        df = df[['subj','trial','cardnumber','trial_type','reward_type','response','RT','reward']]
        df.columns = ('Subject','Trial','Cue','Action','Valence','Choice','RT','Outcome')

        ## Update subject.
        df['Subject'] = i
        df['Diagnosis'] = 'HC'

        ## Update condition info.
        df['Valence'] = df.Valence.replace({'win':'Positive', 'avoid':'Negative'})
        df['Action'] = df.Action.replace({'go':'Go', 'nogo':'No-Go'})

        ## Update trial info.
        tally = lambda arr: np.arange(arr.size) + 1
        df['Trial'] += 1
        df['Exposure'] = df.groupby('Cue').Trial.transform(tally)

        ## Update response info.
        df['RT'] = df.RT.replace({-1:np.nan})
        df['Accuracy'] = np.logical_or((df.Action=="Go")&(df.Choice==1),
                                       (df.Action=="No-Go")&(df.Choice==0)).astype(int)

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
    preprocess_2018swart(), 
    preprocess_2019csifcsal()
], sort=False)

## Reorder columns.
data = data[['Study','Subject','Diagnosis','Condition','Trial','Valence','Action','Cue',
             'Exposure','Choice','RT','Accuracy','Outcome']]

## Re-sort rows.
data = data.sort_values(['Study','Subject','Condition','Trial'])

## Save data.
data.to_csv('data.csv', index=False)