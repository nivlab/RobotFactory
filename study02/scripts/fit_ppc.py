## compatible with models 1,2,3,4,5,6

import os
import numpy as np
import scipy as sp
from pandas import read_csv, concat

import numpy as np
from os.path import dirname
from pandas import read_csv
import pandas as pd
from numba import njit
from tqdm import tqdm
import json

### Posterior predictive check.
np.random.seed(47404)

##############################################################

@njit
def inv_logit(x):
    return 1. / (1 + np.exp(-x))

def waic(log_lik):
    ## (lppd - pWAIC)
    ## lppd:  log pointwise predictive density
    ## pWAIC: the effective number of parameters
    lppd = np.log( np.exp(log_lik).mean(axis=0) )
    pwaic = np.var(log_lik, axis=0)
    return lppd - pwaic



##############################################################

### load data
def load_data(model, session):
    '''
    load data itself, retrurn 
    '''
        
    model_num = int(str(model)[0])
    model_ver = str(model)[1]
    
    r = open(os.path.join('stan_data', f's{session}_data.json'))

    # a dictionary
    dd = json.load(r)

    #reformat
    R = np.array(dd['R'])
    V = np.array(dd['V'])
    Y = np.array(dd['Y'])
    S = np.array(dd['S'])
    C = np.array(dd['C'])
    CONTEXT_CONG = np.array(dd['CONTEXT_CONG'])
    OUTCOME_CONG = np.array(dd['OUTCOME_CONG'])
    N = dd['N']
    E = dd['E']
    
    # load dataframe
    data = read_csv(os.path.join('stan_data',f's{session}_dataframe.csv'))

    ## Load results.
    StanFit = read_csv(os.path.join('stan_results', f'm{model}_s{session}.tsv.gz'), sep='\t', compression='gzip')
    #StanFit = read_csv(os.path.join('stan_results', f'm{model}_s{session}.tsv'), sep='\t')

    ## Extract subject-level parameters.
    beta = StanFit.filter(regex='^beta\[').values
    
    beta_P = 0
    beta_GO = 0
    
    if model_num>1:
        beta_P = StanFit.filter(regex='^beta_P').values
        
    if (model_num>2) & (model_ver=='a'):
        beta_GO = StanFit.filter(regex='^beta_GO').values
    
    eta = 0
    eta_gain, eta_loss, eta_cong, eta_incong = 0,0,0,0
    
    if model_num==4:
        eta_gain = StanFit.filter(regex='^eta_gain').values
        eta_loss = StanFit.filter(regex='^eta_loss').values
    
    elif model_num==5:
        eta_cong = StanFit.filter(regex='^eta_cong').values
        eta_incong = StanFit.filter(regex='^eta_incong').values
    
    else:
        eta = StanFit.filter(regex='^eta').values

    
    ## Parameter expansion
    beta_i = beta[:,S-1]
    beta_P_i = 0
    beta_GO_i = 0
    
    if model_num>1:
        beta_P_i = beta_P[:,S-1]
        
    if (model_num>2) & (model_ver=='a'):
        beta_GO_i = beta_GO[:,S-1]
       
    eta_i = 0
    eta_gain_i, eta_loss_i, eta_cong_i, eta_incong_i = 0,0,0,0
    
    if model_num==4:
        eta_gain_i = eta_gain[:,S-1]
        eta_loss_i = eta_loss[:,S-1]
    
    elif model_num==5:
        eta_cong_i = eta_cong[:,S-1]
        eta_incong_i = eta_incong[:,S-1]
    
    else:
        eta_i = eta[:,S-1]

    CONG = np.zeros(E)

    if model_num==5:
        CONG = CONTEXT_CONG
    
    elif model_num==6:
        CONG = OUTCOME_CONG
        

    ## init Q
    Q1 = 0.5 * beta_i
    Q2 = 0.5 * beta_i
    
    return data, [R, V, Y, S, N, E, C, CONG,\
                  beta, beta_P, beta_GO, \
                  eta, eta_gain, eta_loss,\
                  eta_cong, eta_incong,\
                  beta_i, beta_P_i, beta_GO_i,\
                  eta_i, eta_gain_i, eta_loss_i,\
                  eta_cong_i,eta_incong_i,\
                      Q1, Q2]

##############################################################

def get_ppc(data, params):
    
    R, V, Y, S, N, E, C, CONG, beta, beta_P, beta_GO, \
    eta, eta_gain, eta_loss, eta_cong, eta_incong,\
    beta_i, beta_P_i, beta_GO_i, eta_i, eta_gain_i, eta_loss_i,\
    eta_cong_i, eta_incong_i, Q1, Q2 = params
    
    ## Preallocate space.
    Y_pred = np.zeros((N, E)) 
    Y_hat = np.zeros((N, E)) 
    WAIC = np.zeros((N, E))
    
    
    ## Main loop.
    for e in tqdm(range(E)):
        
        
        ## Define bias.
        bias = V[e] * beta_P_i + (1-V[e])*beta_GO_i

        ## Compute choice probability.
        theta = inv_logit(Q1 - Q2 + bias)
        assert (theta<=1).all() and (theta>=0).all(), 'theta val issue'

        ## Define mask.
        mask = np.where(C[e], C[e], np.nan)

        ## Compute choice likelihood (stage 2).
        Y_pred[:,e] = np.where(Y[e], theta, 1-theta).mean(axis=0)*mask

        ## Compute WAIC (stage 2).
        WAIC[:,e] = waic(np.where(Y[e], np.log(theta), np.log(1-theta)))*mask

        ## Simulate choice (stage 2).
        y = np.random.binomial(1, theta)*mask
        Y_hat[:,e] = y.mean(axis=0)

        ## get eta
        tot_eta_i = eta_i + \
                    (V[e] * eta_gain_i) + ((1-V[e]) * eta_loss_i) +\
                    (CONG[e] * eta_cong_i) + ((1-CONG[e]) * eta_incong_i)
         

        ## Update Q-values
        Q1 += Y[e] * tot_eta_i * ( beta_i * R[e] - Q1 )
        Q2 += (1-Y[e]) * tot_eta_i * ( beta_i * R[e] - Q2 )
    
    d_out = data[(data.rt.isna()) | (data.rt>=0.2)].copy()
    d_out['Y_hat'] = Y_hat[~np.isnan(Y_hat)]
    d_out['Y_pred'] = Y_pred[~np.isnan(Y_pred)]
    d_out['waic'] = WAIC[~np.isnan(WAIC)]
    

    return d_out


