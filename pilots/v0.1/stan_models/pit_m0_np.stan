// Pavlovian Instrumental Transfer (PIT) Task
// Model variant 0 (no pooling)
//
// Parameters (2): 
//   - beta: inverse temperature
//   - eta:  learning rate
//
// Notes:
//   - Model is vectorized such that it iterates over all participants/arms
//   - Model requires no missing data 
//   - Requires mapping between participants (N) and data (H)
//   - Isomorphic to Rescorla-Wagner

data {

    // Metadata
    int  H;                         // Number of participants/blocks/arms
    int  T;                         // Number of trials
    
    // Mappings
    int        sub_ix[H];           // Trial-to-participant mapping
    vector[H]  pav_ix;              // Stimulus-to-valence mapping [Gain = 1, Loss = -1]
    
    // Data
    int       Y[T,H];               // Choices (Go = 1, No-Go = 0)
    vector[H] R[T];                 // Rewards (-1, 0, 1)
    
}
transformed data {

    // Number of participants
    int  N = max(sub_ix);

    // Upper limit of inverse tmperature
    real  ul = 20;
    
    // Vectorized choices
    vector[H]  y[T];
    for (i in 1:T) {
        y[i] = to_vector(Y[i]);
    }

}
parameters {
    
    // Individual-level parameters
    vector[N]  beta_pr;             // Inverse temperature
    vector[N]  eta_pr;              // Learning rate

}
transformed parameters {

    vector<lower =   0, upper = ul>[N]  beta;
    vector<lower =   0, upper =  1>[N]  eta;
    
    beta = Phi_approx( beta_pr ) * ul;
    eta  = Phi_approx( eta_pr );
    
}
model {
    
    // Generated quantities
    matrix[H,T]  p  = rep_matrix(0, H, T);   // Go probability
    vector[H]    Q1 = pav_ix * 0.5;          // State-action values (go)
    vector[H]    Q2 = pav_ix * 0.5;          // State-action values (no-go)
    
    // Parameter expansion
    vector[H]  beta_vec = beta[sub_ix];
    vector[H]  eta_vec = eta[sub_ix];
        
    // Individial-level priors
    beta_pr ~ normal(0, 1);
    eta_pr  ~ normal(0, 1);
        
    for (i in 1:T) {
                
        // Compute likelihood of acting (go).
        p[:,i] = inv_logit( beta_vec .* (Q1 - Q2) );

        // Update action value (go).
        Q1 += y[i] .* ( eta_vec .* ( R[i] - Q1 ) );

        // Update action value (no-go).
        Q2 += (1-y[i]) .* ( eta_vec .* ( R[i] - Q2 ) );

    }
        
    // Likelihood
    to_array_1d(Y) ~ bernoulli( to_vector(p) );
        
}
