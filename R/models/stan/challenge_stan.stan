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
  vector[6] mu_pr;                // mean of group-level distribution
  vector<lower=0>[6] sigma;       // sd of group-level distribution
  
  // Subject-level parameters (raw)
  vector[N] epsilon_pr;
  vector[N] eta_pos_pr;
  vector[N] eta_neg_pr;
  vector[N] b_pr;
  vector[N] pi_pr;
  vector[N] V_init_pr;
  
}

transformed parameters{
  
  
  // Subject-level parameters (transformed)
  vector<lower=0, upper=1>[N] epsilon;
  vector[N] eta_pos;
  vector[N] eta_neg;
  vector[N] b;
  vector[N] pi_par;
  vector[N] V_init;

  
  for (i in 1:N){
    epsilon[i] = Phi_approx( mu_pr[1] + sigma[1] * epsilon_pr[i]);
    eta_pos[i] =  mu_pr[2] + sigma[2] * eta_pos_pr[i];
    eta_neg[i] =  mu_pr[3] + sigma[3] * eta_neg_pr[i];
    b[i] =  mu_pr[4] + sigma[4] * b_pr[i];
    pi_par[i] =  mu_pr[5] + sigma[5] * pi_pr[i] * 10;
    V_init[i] = mu_pr[6] + sigma[6] * V_init_pr[i];
  }
}

model{
  
  // Initialise variables
  vector[4] V;
  matrix[4,2] H;
  row_vector[2] H_trial;
  vector[2] policy;
  row_vector[2] score_functionß;
  real delta;
  
  // Group-level priors
  mu_pr ~ normal(0, 1);
  sigma ~ gamma(1, 0.5);
  
  // Subject_level priors
  epsilon_pr ~ normal(0, 1);  
  eta_pos_pr ~ normal(0, 1);  
  eta_neg_pr ~ normal(0, 1);  
  b_pr ~ normal(0, 1);  
  pi_pr ~ normal(0, 1);  
  V_init_pr ~ normal(0, 1);  
  
  // Iterate over trials
  for (t in 1:T){
    
    if (action[t] != -1){
      
      // initialise V and H if first trial
      if (trial[t] == 1){
        V = rep_vector(V_init[subj_ix[t]], 4);
        H = rep_matrix(0, 4, 2);
      }
      
      // calculate prediction error within critic
      delta = outcome[t] - V[state[t]];
      
      // update value of state
      V[state[t]] = V[state[t]] + epsilon[subj_ix[t]] * delta;
      
      // create an effective go bias with pavlovian modulation
      H_trial = H[state[t]];
      H_trial[2] = H_trial[2] + b[subj_ix[t]] + pi_par[subj_ix[t]] * V[state[t]];
      
      // get a predicted choice probability
      policy = softmax(to_vector(H_trial));
      action[t] ~ categorical_logit(policy);
      
      // specify a score function
      score_function = -1 * to_row_vector(policy);
      score_function[action[t]] = 1 - policy[action[t]];
      
      // update the parameters
      if (delta >= 0){
        H[state[t]] = H[state[t]] + eta_pos[subj_ix[t]] * score_function * delta;
      } else{
        H[state[t]] = H[state[t]] + eta_neg[subj_ix[t]] * score_function * delta;
      }
        
    }
  }
  
}

generated quantities {
  
 
}
