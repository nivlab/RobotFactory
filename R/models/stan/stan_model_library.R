#### Model 1 - pgrl ####
#  PGRL
#   - eta (learning rate)
model1_pgrl <- list(
  "model_file" = "model1_pgrl.stan",
  "parameters" = c(
    "mu_pr",
    "eta"
  ),
  "sample_save_name" = "samples_model1_pgrl.Rdata",
  "parameter_save_name" = "model1_pgrl.Rdata"
)

#### Model 2 - go bias ####
#  Go bias only
#   - b (Go bias)
model2_gobias <- list(
  "model_file" = "model2_gobias.stan",
  "parameters" = c(
    "mu_pr",
    "b"
  ),
  "sample_save_name" = "samples_model2_gobias.Rdata",
  "parameter_save_name" = "model2_gobias.Rdata"
)


#### Model 3 - pgrl with go bias ####
#   - eta (Actor learning rate)
#   - b (Go bias)
model3_pgrl_gobias <- list(
  "model_file" = "model3_pgrl_gobias.stan",
  "parameters" = c(
    "mu_pr",
    "eta",
    "b"
  ),
  "sample_save_name" = "samples_model3_pgrl_gobias.Rdata",
  "parameter_save_name" = "model3_pgrl_gobias.Rdata"
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