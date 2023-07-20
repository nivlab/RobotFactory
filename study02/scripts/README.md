# Scripts

Scripts used for analysis. Described in the order in which they ought to be run.

## Descriptions

- Reinforcement learning models (`fit_pgng.py`): fit a reinforcement learning model using Stan.
- Posterior predictive checks & model comparison
  - Pareto smoothed importance sampling (`psis.py`)
  - Posterior predictive checks (`fit_pgng_ppc.py`)
- Reliability analyses
    - Reliability model (`fit_pgng_trt.py`): fit a hierarchical reinforcement learning model for split-half or test-retest reliability analyses using Stan.
    - Reliability summary (`reliabilty.py`): summarize reliability statistics.
    - Reliability comparison (`reliabilty_comp.py`): compare reliability statistics between Experiments 1 & 2.