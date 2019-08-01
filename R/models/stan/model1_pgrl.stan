data {
  
  // Metadata
  int N;                          // total number of subjects
  int T;                          // total number of trials across subjects
  int subj_ix[T];                 // index of subject for trial i
  int trial[T];                   // trial number (within-subject)
  
  // Data
  int action[T];                  // choice data: 1=no action, 2=press(4arm) or leftpress(6arm), 3=rightpress(6arm)
  int state[T];                   // robot number
  int outcome[T];                 // outcome
  
}

parameters{
  
  // Group-level hyperparameters
  vector[1] mu_pr;                // mean of group-level distribution
  vector<lower=0>[1] sigma;       // sd of group-level distribution
  
  // Subject-level parameters (raw)
  vector[N] eta_pr;
}

transformed parameters{
  
  // Subject-level parameters (transformed)
  vector[N] eta;
  
  for (i in 1:N){
    eta[i] =  mu_pr[1] + sigma[1] * eta_pr[i];
  }
}

model{
  
  // Initialise variables
  vector[4] V;
  matrix[4,2] H;
  vector[2] policy;
  row_vector[2] score_function;
  real delta;
  
  // Group-level priors
  mu_pr ~ normal(0, 1);
  sigma ~ gamma(1, 0.5);
  
  // Subject_level priors
  eta_pr ~ normal(0, 1);  
  
  // Iterate over trials
  for (t in 1:T){
    
    if (action[t] != -1){
      
      // initialise V and H if first trial
      if (trial[t] == 1){
        H = rep_matrix(0, 4, 2);
      }

      // get a predicted choice probability
      policy[1] = logistic_cdf(H[state[t],1] - H[state[t],2], 0, 1);
      policy[2] = logistic_cdf(H[state[t],2] - H[state[t],1], 0, 1);
      action[t] ~ categorical_logit(policy);
      
      // specify a score function
      score_function = -1 * to_row_vector(policy);
      score_function[action[t]] = 1 - policy[action[t]];
      
      // update the parameters
      H[state[t]] = H[state[t]] + eta[subj_ix[t]] * score_function * outcome[t];
      
    }
  }
  
}

generated quantities {
  
  
}
