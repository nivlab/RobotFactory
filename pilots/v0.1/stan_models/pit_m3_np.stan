// Pavlovian Instrumental Transfer (PIT) Task
// Model variant 1 (no pooling)
//
// Parameters (5): 
//   - beta:   inverse temperature
//   - eta_q:  learning rate
//   - eta_v:  learning rate
//   - tau:    go bias
//   - nu:     Pavlovian bias
//
// Notes:
//   - Model is vectorized such that it iterates over all participants/arms
//   - Model requires no missing data 
//   - Requires mapping between participants (N) and data (H)

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
    vector[N]  eta_q_pr;            // Learning rate (Q-values)
    vector[N]  eta_v_pr;            // Learning rate (state values)
    vector[N]  tau_pr;              // Go bias
    vector[N]  nu_pr;               // Pavlovian bias

}
transformed parameters {

    vector<lower =  0, upper = ul>[N]  beta;
    vector<lower =  0, upper =  1>[N]  eta_q;
    vector<lower =  0, upper =  1>[N]  eta_v;
    vector<lower = -1, upper =  1>[N]  tau;
    vector<lower = -1, upper =  1>[N]  nu;
    
    beta  = Phi_approx( beta_pr ) * ul;
    eta_q = Phi_approx( eta_q_pr );
    eta_v = Phi_approx( eta_v_pr );
    tau = tanh( tau_pr );
    nu  = tanh( nu_pr );
    
}
model {
    
    // Generated quantities
    matrix[H,T]  p  = rep_matrix(0, H, T);   // Go probability
    vector[H]    Q1 = pav_ix * 0.5;          // State-action values (go)
    vector[H]    Q2 = pav_ix * 0.5;          // State-action values (no-go)
    vector[H]    V  = rep_vector(0, H);      // State values
    
    // Parameter expansion
    vector[H]  beta_vec = beta[sub_ix];
    vector[H]  eta_q_vec = eta_q[sub_ix];
    vector[H]  eta_v_vec = eta_v[sub_ix];
    vector[H]  tau_vec = tau[sub_ix];
    vector[H]  nu_vec  = nu[sub_ix];
        
    // Individial-level priors
    beta_pr   ~ normal(0, 1);
    eta_q_pr  ~ normal(0, 1);
    eta_v_pr  ~ normal(0, 1);
    tau_pr    ~ normal(0, 1);
    nu_pr     ~ normal(0, 1);
    
    for (i in 1:T) {
        
        // Compute likelihood of acting (go).
        p[:,i] = inv_logit( beta_vec .* (Q1 - Q2 + tau_vec + nu_vec .* V ) );

        // Update action value (go).
        Q1 += y[i] .* ( eta_q_vec .* ( R[i] - Q1 ) );

        // Update action value (no-go).
        Q2 += (1-y[i]) .* ( eta_q_vec .* ( R[i] - Q2 ) );
        
        // Update state value.
        V += eta_v_vec .* ( R[i] - V );

    }
        
    // Likelihood
    to_array_1d(Y) ~ bernoulli( to_vector(p) );
        
}
