// Pavlovian Instrumental Transfer (PIT) Task
// Model variant 1 (partial pooling)
//
// Parameters (4): 
//   - rho: reward scale (equivalent to inverse temperature)
//   - eta: learning rate
//   - tau: Go bias
//   - nu:  Pavlovian bias
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
    int  sub_ix[H];                 // Trial-to-participant mapping
    
    // Data
    int       Y[T,H];               // Choices (Go = 1, No-Go = 0)
    vector[H] R[T];                 // Rewards (-1, 0, 1)
    
}
transformed data {

    // Number of participants
    int  N = max(sub_ix);

    // Upper limit of reward scale (inverse tmperature) 
    real  ul = 20;
    
    // Vectorized choices
    vector[H]  y[T];
    for (i in 1:T) {
        y[i] = to_vector(Y[i]);
    }

}
parameters {
    
    // Group-level parameters
    vector[4]  mu_pr;
    vector<lower=0>  sigma;
    
    // Individual-level parameters
    vector[N]  rho_pr;              // Reward scale
    vector[N]  eta_pr;              // Learning rate
    vector[N]  tau_pr;              // Go bias
    vector[N]  nu_pr;               // Pavlovian bias

}
transformed parameters {

    vector<lower= 0, upper=ul>[N]  rho;
    vector<lower= 0, upper= 1>[N]  eta;
    vector<lower=-1, upper= 1>[N]  tau;
    vector<lower=-1, upper= 1>[N]  nu;
    
    rho = Phi_approx( mu_pr[1] + sigma[1] * rho_pr ) * ul;
    eta = Phi_approx( mu_pr[2] + sigma[2] * eta_pr );
    tau = tanh( mu_pr[3] + sigma[3] * tau_pr );
    nu  = tanh( mu_pr[4] + sigma[4] * nu_pr );
    
}
model {
    
    // Generated quantities
    matrix[H,T]  p  = rep_matrix(0, H, T);   // Go probability
    vector[H]    Q1 = rep_vector(0, H);      // State-action values (go)
    vector[H]    Q2 = rep_vector(0, H);      // State-action values (no-go)
    vector[H]    V  = rep_vector(0, H);      // State values
    
    // Parameter expansion
    vector[H]  rho_vec = rho[sub_ix];
    vector[H]  eta_vec = eta[sub_ix];
    vector[H]  tau_vec = tau[sub_ix];
    vector[H]  nu_vec  = nu[sub_ix];
        
    // Group-level priors
    mu_pr ~ normal(0, 1);
    sigma ~ gamma(1, 0.5);
        
    // Individial-level priors
    rho_pr ~ normal(0, 1);
    eta_pr ~ normal(0, 1);
    tau_pr ~ normal(0, 1);
    nu_pr  ~ normal(0, 1);
    
    for (i in 1:T) {
        
        // Compute likelihood of acting (go).
        p[:,i] = inv_logit( Q1 - Q2 + ul * tau_vec + V .* nu_vec );

        // Update action value (go).
        Q1 += y[i] .* ( eta_vec  .* ( rho_vec .* R[i] - Q1 ) );

        // Update action value (no-go).
        Q2 += (1-y[i]) .* ( eta_vec .* ( rho_vec .* R[i] - Q2 ) );

        // Update state value.
        V += eta_vec .* ( rho_vec .* R[i] - V );

    }
        
    // Likelihood
    to_array_1d(Y) ~ bernoulli( to_vector(p) );
        
}
generated quantities {
   
    // Group-level parameters
    vector[4]  mu;
    mu[1] = Phi_approx( mu_pr[1] ) * ul;
    mu[2] = Phi_approx( mu_pr[2] );
    mu[3] = tanh( mu_pr[3] );
    mu[4] = tanh( mu_pr[4] );


}