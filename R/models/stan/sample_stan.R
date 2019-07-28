##### Set-up #####
tic()
# specify number of samples to take, length of warm-up period, and number of chains
n_samples <- 2
n_warmup <- 1
n_chains <- 1

# import libraries
library(here)                                                                                       # for specifying relative paths
library(tictoc)                                                                                     # for timing
library(rstan)

# source stan utilities and model summaries
source(here("models", "stan", "stan_model_library.R"))

# specify model to sample (as specified in model library)
models <- list(
  model_challenge
)

# load data
pid_data <- read.csv(here("dan_data.csv"))
ids <- unique(pid_data$id)

# rework data for stan
stan_data <- list(
  "N" = length(unique(pid_data$id)),
  "T" = dim(pid_data)[1],
  "subj_ix" = sapply(pid_data$id, FUN=function(foo, all_ids){return(which(all_ids %in% foo))}, ids),
  "state" = pid_data$state,
  "action" = pid_data$response,
  "outcome" = pid_data$outcome,
  "trial" = pid_data$trial
)


# set parallel options
rstan_options(auto_write = TRUE)
options(mc.cores=min(n_chains, parallel::detectCores()))

##### Loop over models #####
for (m in 1:length(models)){
  
  # specify model
  model_to_sample <- models[[m]]
  
  ##### Call stan #####
  
  # draw samples and save them to disk
  samples <- stan(file = here("models", "stan", model_to_sample$model_file),   
                  data = stan_data,
                  save_warmup=F,
                  # init = initVals,
                  pars=model_to_sample$parameters,
                  iter=n_samples, 
                  chains=n_chains, 
                  thin=1,
                  # control = list(max_treedepth = 10),
                  warmup = n_warmup  # Default = iter/2
                  # seed = 123  # Setting seed; Default is random seed
  )
  
  # save the samples in a less bulky format
  model_samples <- extract(samples, pars=model_to_sample$parameters)
  save("model_samples", file=here(model_to_sample$sample_save_name))
}
toc()