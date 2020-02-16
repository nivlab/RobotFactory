import os, pystan
import _pickle as pickle
from pandas import DataFrame

def load_model(filepath):
    """Load or precomplile a StanModel object.

    Parameters
    ----------
    filepath : str
        Path to the Stan model.

    Returns
    -------
    StanModel : pystan.StanModel
        Model described in Stan’s modeling language compiled from C++ code.

    Notes
    -----
    If an extensionless filepath is supplied, looks for *.stan or *.txt files for StanCode 
    and *.pkl and *.pickle for StanModels. Otherwise requires a file with one of those four extensions.
    """

    for ext in ['.pkl','.pickle','.stan','.txt']:

        if filepath.endswith(ext):
            break
        elif os.path.isfile(filepath + ext):
            filepath += ext
            break

    if filepath.lower().endswith(('.pkl','.pickle')):

        ## Load pickle object.
        StanModel = pickle.load(open(filepath, 'rb'))

    elif filepath.lower().endswith(('.stan','.txt')):

        ## Precompile StanModel.
        StanModel = pystan.StanModel(file=filepath)

        ## Dump to pickle object.
        f = '.'.join(filepath.split('.')[:-1]) + '.pkl'
        with open(f, 'wb') as f: pickle.dump(StanModel, f)

    else:

        raise IOError('%s not correct filetype.' %filepath)

    return StanModel

def load_fit(filepath):
    """Load a pickled StanFit object.

    Parameters
    ----------
    filepath : str
        Path to the Stan model.
    ext : str
         Extension for saving Stan models.

    Returns
    -------
    StanFit : pystan.StanFit4model
        Model-specific StanFit instance.
    """
    assert os.path.isfile(filepath)
    with open(filepath, 'rb') as fn: fit = pickle.load(fn, encoding='bytes')
    return fit

def save_fit(filepath, StanFit, data=None, summary=True, ext='pkl'):
    """Save StanFit samples to disk.

    Parameters
    ----------
    filepath : str
        Path to save file.
    StanFit : pystan.StanFit4model
        Model-specific StanFit instance.
    data : dict
        A Python dictionary providing the data for the model.
    """

    ## Define output paths.
    if filepath.endswith(ext):
        summpath = filepath.replace(ext,'csv')
    else:
        summpath = '%s.csv' %filepath
        filepath = '%s.%s' %(filepath, ext)

    ## Save summary file.
    if summary:
        summary = StanFit.summary()
        summary = DataFrame(summary['summary'], columns=summary['summary_colnames'],
                            index=summary['summary_rownames'])
        summary.to_csv(summpath)

    ## Save contents of StanFit.
    samples = StanFit.extract()
    if data is not None:
        for k, v in data.items(): samples[k] = v

    with open(filepath, 'wb') as fn: pickle.dump(samples, fn)