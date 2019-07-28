#### Model 1 ####
# TD(0) actor-critic
#   pars: - eta (actor learning rate)
#         - epsilon (critic learning rate)
model_AC <- list("likelihood" = likelihood_AC,
                 "pars" = list("epsilon" = NA,
                               "eta" = NA,
                               "V_init" = NA,
                               "H_init" = NA),
                 "lower_bound" = c(0,0,-Inf,-Inf),
                 "upper_bound" = c(Inf,Inf,Inf,Inf),
                 "lambda" = function(epsilon,eta,V_init,H_init){
                   model$pars$epsilon <- epsilon
                   model$pars$eta <- eta
                   model$pars$V_init <- V_init
                   model$pars$H_init <- H_init
                   ll <- model$likelihood(model, fit_data)
                   return(ll$neg_ll)
                 },
                 "start_points" = function(n_starts = 1){
                   return(list("epsilon" = runif(n_starts, min = 0, max = 1),
                               "eta" = runif(n_starts, min = 0, max = 1),
                               "V_init" = runif(n_starts, min=-0.5, max=0.5)))},
                 "fixed" = list("H_init" = H_init_constant)
)

#### Model 2 ####
# TD(0) actor-critic with a go bias
#   pars: - eta (actor learning rate)
#         - epsilon (critic learning rate)
#         - b (go bias)
model_AC_go <- list("likelihood" = likelihood_AC_go,
                 "pars" = list("epsilon" = NA,
                               "eta" = NA,
                               "b" = NA,
                               "V_init" = NA,
                               "H_init" = NA),
                 "lower_bound" = c(0,0,-Inf,-Inf,-Inf),
                 "upper_bound" = c(Inf,Inf,Inf,Inf,Inf),
                 "lambda" = function(epsilon,eta,b,V_init,H_init){
                   model$pars$epsilon <- epsilon
                   model$pars$eta <- eta
                   model$pars$b <- b
                   model$pars$V_init <- V_init
                   model$pars$H_init <- H_init
                   ll <- model$likelihood(model, fit_data)
                   return(ll$neg_ll)
                 },
                 "start_points" = function(n_starts = 1){
                   return(list("epsilon" = runif(n_starts, min = 0, max = 1),
                               "eta" = runif(n_starts, min = 0, max = 1),
                               "b" = runif(n_starts, min=-5, max=5),
                               "V_init" = runif(n_starts, min=-0.5, max=0.5)))},
                 "fixed" = list("H_init" = H_init_constant)
)

#### Model 3 ####
# TD(0) actor-critic with a go bias and pavlovian transfer
#   pars: - eta (actor learning rate)
#         - epsilon (critic learning rate)
#         - b (go bias)
#         - pi (modulation of go bias by pavlovian value of state)
model_AC_go_transfer <- list("likelihood" = likelihood_AC_go_transfer,
                    "pars" = list("epsilon" = NA,
                                  "eta" = NA,
                                  "b" = NA,
                                  "pi" = NA,
                                  "V_init" = NA,
                                  "H_init" = NA),
                    "lower_bound" = c(0,0,-Inf,-Inf,-Inf,-Inf),
                    "upper_bound" = c(Inf,Inf,Inf,Inf,Inf,Inf),
                    "lambda" = function(epsilon,eta,b,pi,V_init,H_init){
                      model$pars$epsilon <- epsilon
                      model$pars$eta <- eta
                      model$pars$b <- b
                      model$pars$pi <- pi
                      model$pars$V_init <- V_init
                      model$pars$H_init <- H_init
                      ll <- model$likelihood(model, fit_data)
                      return(ll$neg_ll)
                    },
                    "start_points" = function(n_starts = 1){
                      return(list("epsilon" = runif(n_starts, min = 0, max = 1),
                                  "eta" = runif(n_starts, min = 0, max = 1),
                                  "b" = runif(n_starts, min=-5, max=5),
                                  "pi" = runif(n_starts, min=-5, max=5),
                                  "V_init" = runif(n_starts, min=-0.5, max=0.5)))},
                    "fixed" = list("H_init" = H_init_constant)
)

#### Model 4 ####
# Q-learning
#   pars: - beta (softmax inverse temperature)
#         - epsilon (learning rate)
model_Q <- list("likelihood" = likelihood_Q,
                             "pars" = list("epsilon" = NA,
                                           "beta" = NA,
                                           "V_init" = NA,
                                           "H_init" = NA),
                             "lower_bound" = c(0,0,-Inf,-Inf),
                             "upper_bound" = c(Inf,Inf,Inf,Inf),
                             "lambda" = function(epsilon,beta,Q_init){
                               model$pars$epsilon <- epsilon
                               model$pars$beta <- beta
                               model$pars$Q_init <- Q_init
                               ll <- model$likelihood(model, fit_data)
                               return(ll$neg_ll)
                             },
                             "start_points" = function(n_starts = 1){
                               return(list("epsilon" = runif(n_starts, min = 0, max = 1),
                                           "beta" = runif(n_starts, min = 0, max = 5)))},
                             "fixed" = list("Q_init" = Q_init_constant)
)

#### Model 5 ####
# Q-learning with a go bias
#   pars: - beta (softmax inverse temperature)
#         - epsilon (learning rate)
#         - b (go bias)
model_Q_go <- list("likelihood" = likelihood_Q_go,
                "pars" = list("epsilon" = NA,
                              "beta" = NA,
                              "b" = NA,
                              "Q_init" = NA,
                              "H_init" = NA),
                "lower_bound" = c(0,0,-Inf,-Inf,-Inf),
                "upper_bound" = c(Inf,Inf,Inf,Inf,Inf),
                "lambda" = function(epsilon,beta,b,Q_init){
                  model$pars$epsilon <- epsilon
                  model$pars$beta <- beta
                  model$pars$b <- b
                  model$pars$Q_init <- Q_init
                  ll <- model$likelihood(model, fit_data)
                  return(ll$neg_ll)
                },
                "start_points" = function(n_starts = 1){
                  return(list("epsilon" = runif(n_starts, min = 0, max = 1),
                              "beta" = runif(n_starts, min = 0, max = 5),
                              "b" = runif(n_starts,min=-1,max=1)))},
                "fixed" = list("Q_init" = Q_init_constant)
)

#### Model 6 ####
# TD(0) actor-critic with a go bias, pavlovian transfer, and asymmetric learning in the critic
#   pars: - eta_pos (actor learning rate for positive RPEs)
#         - eta_neg (actor learning rate for negative RPEs)
#         - epsilon (critic learning rate)
#         - b (go bias)
#         - pi (modulation of go bias by pavlovian value of state)
model_AC_go_transfer_asymma <- list("likelihood" = likelihood_AC_go_transfer_asymma,
                             "pars" = list("epsilon" = NA,
                                           "eta_pos" = NA,
                                           "eta_neg" = NA,
                                           "b" = NA,
                                           "pi" = NA,
                                           "V_init" = NA,
                                           "H_init" = NA),
                             "lower_bound" = c(0,0,0,-Inf,-Inf,-Inf,-Inf),
                             "upper_bound" = c(Inf,Inf,Inf,Inf,Inf,Inf,Inf),
                             "lambda" = function(epsilon,eta_pos,eta_neg,b,pi,V_init,H_init){
                               model$pars$epsilon <- epsilon
                               model$pars$eta_pos <- eta_pos
                               model$pars$eta_neg <- eta_neg
                               model$pars$b <- b
                               model$pars$pi <- pi
                               model$pars$V_init <- V_init
                               model$pars$H_init <- H_init
                               ll <- model$likelihood(model, fit_data)
                               return(ll$neg_ll)
                             },
                             "start_points" = function(n_starts = 1){
                               return(list("epsilon" = runif(n_starts, min = 0, max = 1),
                                           "eta_pos" = runif(n_starts, min = 0, max = 1),
                                           "eta_neg" = runif(n_starts, min = 0, max = 1),
                                           "b" = runif(n_starts, min=-5, max=5), 
                                           "pi" = runif(n_starts, min=-5, max=5),
                                           "V_init" = runif(n_starts, min=-0.5, max=0.5)))},
                             "fixed" = list("H_init" = H_init_constant)
)