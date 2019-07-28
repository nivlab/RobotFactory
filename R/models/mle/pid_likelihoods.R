likelihood_AC <- function(model, data){
  
  # specify constants
  V_init <- model$pars$V_init
  H_init <- model$pars$H_init
  n_states <- length(unique(data$state))
  n_actions <- sum(unique(data$response) > 0)
  n_trials <- max(data$trial)
  
  # set up containers 
  V <- rep(V_init, times=n_states)                              # state value vector
  H <- matrix(data=H_init, nrow=n_states, ncol=n_actions)       # policy matrix
  pr_choice <- rep(NA, times=n_trials)                          # choice probability container
  
  # loop over trials
  for (i in 1:n_trials){
    
    state <- data[i,]$state
    action <- data[i,]$response
    outcome <- data[i,]$outcome
    
    if (!(action == -1)){
      
      # get TD prediction error
      delta <- outcome - V[state]
      
      # update value of state
      V[state] <- V[state] + model$pars$epsilon * (delta)
      
      # get a predicted choice probability
      policy <- exp(H[state,]) / sum(exp(H[state,]))
      
      # extract the choice probability for the chosen action
      pr_choice[i] <- policy[action]

      # get a score function for the chosen action
      score_function <- -policy
      score_function[action] <- 1 - policy[action]
      
      # update the policy parameters
      H[state,] <- H[state,] + model$pars$eta * score_function * delta
      
    }
    
  }
  
  # return choice probabilities and negative log likelihood
  neg_ll <- sum(-log(pr_choice), na.rm=T)
  if (is.infinite(neg_ll)){
    neg_ll <- 1e20
  }
  
  # print(model$pars$epsilon)
  # print(model$pars$eta)
  # print(neg_ll)
  return(
    list(
      "pr_choice" = pr_choice,
      "neg_ll" = neg_ll
    )
  )
}

likelihood_AC_go <- function(model, data){
  
  # specify constants
  V_init <- model$pars$V_init
  H_init <- model$pars$H_init
  n_states <- length(unique(data$state))
  n_actions <- sum(unique(data$response) > 0)
  n_trials <- max(data$trial)
  
  # set up containers 
  V <- rep(V_init, times=n_states)                              # state value vector
  H <- matrix(data=H_init, nrow=n_states, ncol=n_actions)       # policy matrix
  pr_choice <- rep(NA, times=n_trials)                          # choice probability container
  
  # loop over trials
  for (i in 1:n_trials){
    
    state <- data[i,]$state
    action <- data[i,]$response
    outcome <- data[i,]$outcome
    
    if (!(action == -1)){
      
      # get TD prediction error
      delta <- outcome - V[state]
      
      # update value of state
      V[state] <- V[state] + model$pars$epsilon * (delta)
      
      # create an effective go bias
      H_eff <- H[state,]
      H_eff[2] <- H_eff[2] + model$pars$b
      if (n_states == 6){
        H_eff[3] <- H_eff[3] + model$pars$b
      }
      
      # get a predicted choice probability
      policy <- exp(H_eff) / sum(exp(H_eff))
      
      # extract the choice probability for the chosen action
      pr_choice[i] <- policy[action]
      
      # get a score function for the chosen action
      score_function <- -policy
      score_function[action] <- 1 - policy[action]
      
      # update the policy parameters
      H[state,] <- H[state,] + model$pars$eta * score_function * delta
      
    }
    
  }
  
  # return choice probabilities and negative log likelihood
  neg_ll <- sum(-log(pr_choice), na.rm=T)
  if (is.infinite(neg_ll)){
    neg_ll <- 1e20
  }
  
  # print(model$pars$epsilon)
  # print(model$pars$eta)
  # print(neg_ll)
  return(
    list(
      "pr_choice" = pr_choice,
      "neg_ll" = neg_ll
    )
  )
}

likelihood_AC_go_transfer <- function(model, data){
  
  # specify constants
  V_init <- model$pars$V_init
  H_init <- model$pars$H_init
  n_states <- length(unique(data$state))
  n_actions <- sum(unique(data$response) > 0)
  n_trials <- max(data$trial)
  
  # set up containers 
  V <- rep(V_init, times=n_states)                              # state value vector
  H <- matrix(data=H_init, nrow=n_states, ncol=n_actions)       # policy matrix
  pr_choice <- rep(NA, times=n_trials)                          # choice probability container
  
  # loop over trials
  for (i in 1:n_trials){
    
    state <- data[i,]$state
    action <- data[i,]$response
    outcome <- data[i,]$outcome
    
    if (!(action == -1)){
      
      # get TD prediction error
      delta <- outcome - V[state]
      
      # update value of state
      V[state] <- V[state] + model$pars$epsilon * (delta)
      
      # create an effective go bias with pavlovian modulation
      H_eff <- H[state,]
      H_eff[2] <- H_eff[2] + model$pars$b + model$pars$pi * V[state]
      if (n_states == 6){
        H_eff[3] <- H_eff[3] + model$pars$b + model$pars$pi * V[state]
      }
      
      # get a predicted choice probability
      policy <- exp(H_eff) / sum(exp(H_eff))
      
      # extract the choice probability for the chosen action
      pr_choice[i] <- policy[action]
      
      # get a score function for the chosen action
      score_function <- -policy
      score_function[action] <- 1 - policy[action]
      
      # update the policy parameters
      H[state,] <- H[state,] + model$pars$eta * score_function * delta
      
    }
    
  }
  
  # return choice probabilities and negative log likelihood
  neg_ll <- sum(-log(pr_choice), na.rm=T)
  if (is.infinite(neg_ll)){
    neg_ll <- 1e20
  }
  
  # print(model$pars$epsilon)
  # print(model$pars$eta)
  # print(neg_ll)
  return(
    list(
      "pr_choice" = pr_choice,
      "neg_ll" = neg_ll
    )
  )
}

likelihood_Q <- function(model, data){
  
  # specify constants
  Q_init <- model$pars$H_init
  n_states <- length(unique(data$state))
  n_actions <- sum(unique(data$response) > 0)
  n_trials <- max(data$trial)
  
  # set up containers 
  Q <- matrix(data=H_init, nrow=n_states, ncol=n_actions)       # policy matrix
  pr_choice <- rep(NA, times=n_trials)                          # choice probability container
  
  # loop over trials
  for (i in 1:n_trials){
    
    state <- data[i,]$state
    action <- data[i,]$response
    outcome <- data[i,]$outcome
    
    if (!(action == -1)){
      
      # get a predicted choice probability
      policy <- exp(model$pars$beta * Q[state,]) / sum(exp(model$pars$beta * Q[state,]))
      
      # extract the choice probability for the chosen action
      pr_choice[i] <- policy[action]
      
      # get TD prediction error
      delta <- outcome - Q[state,action]
      
      # update value of state
      Q[state,action] <- Q[state,action] + model$pars$epsilon * (delta)

      
    }
    
  }
  
  # return choice probabilities and negative log likelihood
  neg_ll <- sum(-log(pr_choice), na.rm=T)
  if (is.infinite(neg_ll)){
    neg_ll <- 1e20
  }

  print(neg_ll)
  return(
    list(
      "pr_choice" = pr_choice,
      "neg_ll" = neg_ll
    )
  )
}

likelihood_Q_go <- function(model, data){
  
  # specify constants
  Q_init <- model$pars$H_init
  n_states <- length(unique(data$state))
  n_actions <- sum(unique(data$response) > 0)
  n_trials <- max(data$trial)
  
  # set up containers 
  Q <- matrix(data=H_init, nrow=n_states, ncol=n_actions)       # policy matrix
  pr_choice <- rep(NA, times=n_trials)                          # choice probability container
  
  # loop over trials
  for (i in 1:n_trials){
    
    state <- data[i,]$state
    action <- data[i,]$response
    outcome <- data[i,]$outcome
    
    if (!(action == -1)){
      
      # get a predicted choice probability
      W <- Q[state,]
      W[2] <- W[2] + model$pars$b
      if (n_states == 6){
        W[3] <- W[3] + model$pars$b
      }
      policy <- exp(model$pars$beta * W) / sum(exp(model$pars$beta * W))
      
      # extract the choice probability for the chosen action
      pr_choice[i] <- policy[action]
      
      # get TD prediction error
      delta <- outcome - Q[state,action]
      
      # update value of state
      Q[state,action] <- Q[state,action] + model$pars$epsilon * (delta)
      
      
    }
    
  }
  
  # return choice probabilities and negative log likelihood
  neg_ll <- sum(-log(pr_choice), na.rm=T)
  if (is.infinite(neg_ll)){
    neg_ll <- 1e20
  }
  
  # print(model$pars$epsilon)
  # print(model$pars$eta)
  # print(neg_ll)
  return(
    list(
      "pr_choice" = pr_choice,
      "neg_ll" = neg_ll
    )
  )
}

likelihood_AC_go_transfer_asymma <- function(model, data){
  
  # specify constants
  V_init <- model$pars$V_init
  H_init <- model$pars$H_init
  n_states <- length(unique(data$state))
  n_actions <- sum(unique(data$response) > 0)
  n_trials <- max(data$trial)
  
  # set up containers 
  V <- rep(V_init, times=n_states)                              # state value vector
  H <- matrix(data=H_init, nrow=n_states, ncol=n_actions)       # policy matrix
  pr_choice <- rep(NA, times=n_trials)                          # choice probability container
  
  # loop over trials
  for (i in 1:n_trials){
    
    state <- data[i,]$state
    action <- data[i,]$response
    outcome <- data[i,]$outcome
    
    if (!(action == -1)){
      
      # get TD prediction error
      delta <- outcome - V[state]
      
      # update value of state
      V[state] <- V[state] + model$pars$epsilon * (delta)
      
      # create an effective go bias
      H_eff <- H[state,]
      H_eff[2] <- H_eff[2] + model$pars$b + model$pars$pi * V[state]
      if (n_states == 6){
        H_eff[3] <- H_eff[3] + model$pars$b + model$pars$pi * V[state]
      }
      
      # get a predicted choice probability
      policy <- exp(H_eff) / sum(exp(H_eff))
      
      # extract the choice probability for the chosen action
      pr_choice[i] <- policy[action]
      
      # get a score function for the chosen action
      score_function <- -policy
      score_function[action] <- 1 - policy[action]
      
      # update the policy parameters
      if (delta >= 0){
        eta <- model$pars$eta_pos
      } else{
        eta <- model$pars$eta_neg
      }
      
      H[state,] <- H[state,] + eta * score_function * delta
      
    }
    
  }
  
  # return choice probabilities and negative log likelihood
  neg_ll <- sum(-log(pr_choice), na.rm=T)
  if (is.infinite(neg_ll)){
    neg_ll <- 1e20
  }
  
  # print(neg_ll)
  return(
    list(
      "pr_choice" = pr_choice,
      "neg_ll" = neg_ll
    )
  )
}
