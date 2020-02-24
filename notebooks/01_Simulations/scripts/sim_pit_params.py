import numpy as np

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Simulate parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define metadata.
n_agents = 1000

## Simulate parameters.
beta = np.random.uniform( 4.0, 8.0, n_agents)
eta  = np.random.uniform( 0.1, 0.4, n_agents)
tau  = np.random.uniform(-0.1, 0.3, n_agents)
nu   = np.random.uniform( 0.2, 0.6, n_agents)

## Save.
params = np.column_stack([beta,eta,tau,nu])
np.savez_compressed('params.npz', params=params)