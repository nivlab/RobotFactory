# import packages
library(tictoc)
library(here)
library(stats4)

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

