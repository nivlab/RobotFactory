#### preliminaries ####

# import packages
library(tictoc)
library(here)
library(stats4)

# load data
pit_data <- read.csv(here("dan_data.csv"))

# extract ids
ids <- unique(pit_data$id)
n_participants <- length(unique(ids))

# set details of fitting
n_starts <- 3                     # number of independent start points to try for mle fitting

# specify constants
Q_init_constant <- 0
H_init_constant <- 0

#### source and set up models ####

# source models and likelihoods
source(here("models","mle","pid_likelihoods.R"))
source(here("models","mle","pid_model_library.R"))

# specify model
model <- model_Q

# specify containers
pars <- array(data = NA, dim = c(n_participants, length(model$par)))
mean_prob <- rep(NA, times = n_participants)
neg_ll <- rep(NA, times = n_participants)

#### loop over participants ####
for (p in 1:n_participants){
  
  exit_loop <- FALSE
  start_counter <- 0
  best_ll <- Inf
  
  while (!exit_loop){
    print(sprintf("Participant %.0f of %.0f, start %.0f of %.0f", p, n_participants, start_counter + 1, n_starts))    
    
    tryCatch({
      # mark the participant getting fit  
      
      # specify data
      fit_data <- subset(pit_data, pit_data$id == ids[p])
      
      # fit model
      fit <- mle(model$lambda,
                 method = "L-BFGS-B",
                 start = model$start_point(),
                 lower = model$lower_bound,
                 upper = model$upper_bound,
                 fixed = model$fixed)
      
      # assign parameters to model for testing
      for (n in 1:length(names(fit@fullcoef))){
        model$pars[names(fit@fullcoef)[n]] <- fit@fullcoef[names(fit@fullcoef)[n]]
      }
      
      fit_ll <- model$likelihood(model, fit_data)
      if (fit_ll$neg_ll < best_ll){
        neg_ll[p] <- fit_ll$neg_ll
        pars[p,] <- unlist(model$pars)
        mean_prob[p] <- mean(fit_ll$pr_choice, na.rm=T)
        best_ll <- fit_ll$neg_ll
      }
      
      start_counter <- start_counter + 1
      if (start_counter >= n_starts){
        exit_loop <- TRUE
        print(neg_ll[p])
        print(pars[p,])
      }
    }, error = function(err){
      print(sprintf("Error on participant %.0f",p))
    })
  }
  
}
