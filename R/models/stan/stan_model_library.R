#### Model 1 ####
#  PGRL
#   - beta (softmax inverse temperature)
model1_pgrl <- list(
  "model_file" = "model1_pgrl.stan",
  "parameters" = c(
    "mu_pr",
    "eta"
  ),
  "sample_save_name" = "samples_model1_pgrl.Rdata",
  "parameter_save_name" = "model1_pgrl.Rdata"
)

#### Model A ####
#  Null model
#   - beta (softmax inverse temperature)
model_challenge <- list(
  "model_file" = "challenge_stan.stan",
  "parameters" = c(
    "mu_pr",
    "epsilon",
    "eta_pos",
    "eta_neg",
    "b",
    "pi_par",
    "V_init"
  ),
  "sample_save_name" = "challenge_samples.Rdata",
  "parameter_save_name" = "challenge_null.Rdata"
)