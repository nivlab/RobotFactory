import numpy as np
from numba import njit

@njit
def inv_logit(arr):
    """Fast inverse logistic function."""
    return 1. / (1. + np.exp(-arr))

def hdi(arr, density=0.95):
    '''Finds the highest density interval from a sample of values.
    
    Parameters
    ----------
    arr : array
        MCMC samples.
    density : float
        A scalar between 0 and 1, indicating the mass within the credible
        interval that is to be estimated.
   
    Returns
    -------
    lb, ub : floats
        Lower and upper bounds of the highest density interval.
    
    References
    ----------
    [1] Kruschke, J. (2014). Doing Bayesian data analysis: A tutorial with R, JAGS,
        and Stan. Academic Press.
        https://sites.google.com/site/doingbayesiandataanalysis/
    '''

    sortedPts = np.sort(arr)
    ciIdxInc = np.ceil(density * len( sortedPts )).astype(int)
    nCIs = len( sortedPts ) - ciIdxInc
    ciWidth = [ sortedPts[ i + ciIdxInc ] - sortedPts[ i ] for i in np.arange(nCIs).astype(int) ]
    HDImin = sortedPts[ np.argmin( ciWidth ) ]
    HDImax = sortedPts[ np.argmin( ciWidth ) + ciIdxInc ]
    return HDImin, HDImax

def waic(log_lik):
    """Widely applicable information criterion.
    
    Parameters
    ----------
    log_lik : array, shape=(n_samples, n_obs)
        Log-likelihood values of model
  
    Returns
    -------
    waic : float
        Widely applicable information criterion.
    
    References
    ----------
    [1] Watanabe, S. (2010). Asymptotic equivalence of Bayes cross validation and
        widely applicable information criterion in singular learning theory. Journal
        of Machine Learning Research, 11(Dec), 3571-3594.
    [2] Vehtari, A., Gelman, A., & Gabry, J. (2017). Practical Bayesian model
        evaluation using leave-one-out cross-validation and WAIC. Statistics and
        Computing, 27(5), 1413–1432.
    """

    lppd = np.log( np.exp(log_lik).mean(axis=0) )
    pwaic = np.var(log_lik, axis=0)
    return lppd - pwaic

def posterior_predictive_ck(samples, simulate=False, seed=0):
    """Posterior predictive check for choice kernel models.
    
    Parameters
    ----------
    samples : OrderedDict
        Samples returned by a StanFit object.
        
    Returns
    -------
    log_lik : array, shape (n_samp, n_trials, n_stim)
        Predicted log-likelihood.
        
    Notes
    -----
    Samples should include the data (Y) and subject index (sub_ix)
    required by the Stan model. 
    """
    np.random.seed(seed)
    
    ## Extract data.
    Y = samples['Y']
    sub_ix = samples['sub_ix'] - 1

    ## Extract parameters.
    beta = samples['beta']
    eta  = samples['eta']

    ## Define metadata.
    S, N = beta.shape
    T, H = Y.shape 

    ## Initialize state-action values.
    Q1 = 0.5 * np.ones((S,H))
    Q2 = 0.5 * np.ones((S,H))
    
    ## Preallocate space.
    log_lik = np.zeros((S,T,H))
    Y_pred  = np.zeros((S,T,H))

    for i in range(Y.shape[0]):

        ## Compute likelihood of acting (go).
        p = inv_logit( beta[:,sub_ix] * (Q1 - Q2) )

        ## Compute log-likelihood.
        log_lik[:,i,:] = np.log(Y[i] * p + (1-Y[i]) * (1-p))

        ## Simulate predicted choice.
        if simulate: Y_pred[:,i,:] = np.random.binomial(1, p)
        
        ## Update action value (go).
        Q1 += eta[:,sub_ix] * ( Y[i] - Q1 )

        ## Update action value (no-go).
        Q2 += eta[:,sub_ix] * ( (1-Y[i]) - Q2 )
    
    if simulate: return log_lik, Y_pred
    else: return log_lik
    
def posterior_predictive_pit(samples, simulate=False, seed=0):
    """Posterior predictive check for the Pavlovian instrumental transfer models.
    
    Parameters
    ----------
    samples : OrderedDict
        Samples returned by a StanFit object.
        
    Returns
    -------
    log_lik : array, shape (n_samp, n_trials, n_stim)
        Predicted log-likelihood.
        
    Notes
    -----
    Samples should include the data (Y) and subject index (sub_ix)
    required by the Stan model. 
    """
    np.random.seed(seed)
    
    ## Define metadata.
    S = samples['lp__'].size
    H = samples['H']
    T = samples['T']
    N = samples['sub_ix'].max()

    ## Extract data.
    Y = samples['Y']
    R = samples['R']
    
    ## Extract mappings.
    sub_ix = samples['sub_ix'] - 1    # 0-indexing
    pav_ix = samples['pav_ix']
    z = np.where(pav_ix > 0, 1, 0)

    ## Extract and expand inverse temperatures.
    if 'beta' in samples.keys():
        beta_p = samples.get('beta')[:,sub_ix]
        beta_n = samples.get('beta')[:,sub_ix]
    else:
        beta_p = samples.get('beta_p')[:,sub_ix]
        beta_n = samples.get('beta_n')[:,sub_ix]
    beta = z * beta_p + (1-z) * beta_n

    ## Extract and expand learning rates.
    if 'eta' in samples.keys():
        eta_q = samples.get('eta')[:,sub_ix]
        eta_v = np.zeros_like(eta_q)
    else:
        eta_q = samples.get('eta_q')[:,sub_ix]
        eta_v = samples.get('eta_v')[:,sub_ix]
    
    ## Extract and expand biases.
    tau = samples.get('tau', np.zeros((S,N)))[:,sub_ix]
    nu  = samples.get('nu',  np.zeros((S,N)))[:,sub_ix]
    
    ## Initialize state-action values.
    Q1 = np.zeros((S,H)) + np.copy(pav_ix * 0.5)
    Q2 = np.zeros((S,H)) + np.copy(pav_ix * 0.5)
    
    ## Initialize state values.
    V = np.zeros((S,H))
    if not np.any(eta_v): V += np.copy(pav_ix)
    
    ## Preallocate space.
    log_lik = np.zeros((S,T,H))
    Y_pred  = np.zeros((S,T,H))

    for i in range(Y.shape[0]):

        ## Compute likelihood of acting (go).
        p = inv_logit( beta * (Q1 - Q2 + tau + nu * V ) )

        ## Compute log-likelihood.
        log_lik[:,i,:] = np.log(Y[i] * p + (1-Y[i]) * (1-p))

        ## Simulate predicted choice.
        if simulate: Y_pred[:,i,:] = np.random.binomial(1, p)
        
        ## Update action value (go).
        Q1 += Y[i] * ( eta_q * ( R[i] - Q1 ) )

        ## Update action value (no-go).
        Q2 += (1-Y[i]) * ( eta_q * ( R[i] - Q2 ) )
        
        ## Update state action values.
        V += eta_v * (R[i] - V)
    
    if simulate: return log_lik, Y_pred
    else: return log_lik