"""Tools for modeling the human Pavlovian Instrumental Transfer task."""

__version__ = '0.2'

from .agents import (inv_logit, softmax, phi_approx, AgentsPIT)
from .io import (load_model, load_fit, save_fit)
from .posterior import (hdi, waic, posterior_predictive_ck, posterior_predictive_pit)
