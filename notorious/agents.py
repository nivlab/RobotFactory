import numpy as np
from numba import njit

@njit
def inv_logit(arr):
    """Fast inverse logistic function."""
    return 1. / (1. + np.exp(-arr))

@njit
def softmax(arr):
    """Scale-robust softmax function"""
    arr = np.exp(arr - np.max(arr))
    return arr / arr.sum()

@njit
def phi_approx(arr):
    '''Elementwise fast approximation of the cumulative unit normal.'''
    return inv_logit(0.07056 * arr ** 3 + 1.5976 * arr)

def _resize(x, size):
    """Convenience function"""
    x = np.atleast_1d(np.copy(x))
    
    if x.size == size:
        return x
    elif x.size == 1:
        return np.repeat(x, size)
    else:
        raise ValueError('Array size mismatch.')

class AgentsPIT(object):
    """Pavlovian instrumental transfer bots.
    
    Parameters
    ----------
    beta : float | array
        Inverse temperature.
    eta : float | array
        Learning rate (between 0 & 1).
    tau : float | array
        Go bias.
    nu : float | array
        Pavlovian bias.
    w : float | array
        Reframing ability (between 0 & 1).
    v0 : float
        Initial state value.
    n_agents: int
        Number of agents to simulate (defaults to size of input parameters).
    """
    
    def __init__(self, beta, eta, tau, nu, w, v0=0, n_agents=None):        
        
        ## Define metadata.
        if n_agents is None: n_agents = max([np.size(x) for x in [beta,eta,tau,nu,w]])
        self.n_agents = n_agents
        self._ix = np.arange(self.n_agents).astype(int)
        
        ## Define parameters.
        self.beta = _resize(beta, self.n_agents)
        self.eta  = _resize(eta,  self.n_agents)
        self.tau  = _resize(tau,  self.n_agents)
        self.nu   = _resize(nu,   self.n_agents)
        self.w    = _resize(w,    self.n_agents)
        
        ## Initialize Q-values.
        self.Q = np.zeros((self.n_agents, 2), dtype=float)
        self.V = np.ones(self.n_agents, dtype=float) * v0
        
    def __repr__(self):
        return f'<PIT agents (N = {self.n_agents})>'
        
    def train(self, R):
        """Train agents on Pavlovian Instrumental Transfer task.
        
        Parameters
        ----------
        R : ndarray, shape (n_agents, n_trials, 2)
            Outcome for each action.
            
        Returns
        -------
        Y : ndarray, shape (n_agents, n_trials)
            Chosen action (go = 1, no-go = 0).
        """
        
        ## Error-catching.
        n_agents, n_trials, n_bandits = R.shape
        assert n_agents == self.n_agents
        assert n_bandits == 2

        ## Preallocate space.
        Y = np.ones((n_agents, n_trials), dtype=int)
        
        ## Main loop.
        for i in range(n_trials):
        
            ## Action selection.
            dEV = self.Q[:,1] - self.Q[:,0] + self.tau + self.nu * np.mean(self.Q, axis=1)
            theta = inv_logit( self.beta * dEV  )
            Y[:,i] = np.random.binomial(1, theta)

            ## Observe outcomes.
            r = R[self._ix, i, Y[:,i]]
            
            ## Update action-values.
            self.Q[self._ix, Y[:,i]] += self.eta * ( (r - (self.w * self.V)) - self.Q[self._ix, Y[:,i]] )
            
            ## Update state-values.
            self.V += self.eta * (r - self.V)
        
        return Y