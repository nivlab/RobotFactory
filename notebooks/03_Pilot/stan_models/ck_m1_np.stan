// Choice Kernel
// Model variant 1 (no pooling)
//
// Parameters (2): 
//   - beta: inverse temperature
//   - eta:  learning rate
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

    // Individual-level parameters
    vector[N]  beta_pr;             // Inverse temperature
    vector[N]  eta_pr;              // Learning rate

}
transformed parameters {

    // Individual-level parameters
    vector[N]  beta;
    vector[N]  eta_pr;
    
    beta = Phi_approx( beta_pr ) * ul;
    eta  = Phi_approx( eta_pr );

}
data {

    // Generated quantities
    matrix[H,T]  p  = rep_matrix(0, H, T);   // Go probability
    vector[H]    Q1 = rep_vector(0, H);      // State-action values (go)
    vector[H]    Q2 = rep_vector(0, H);      // State-action values (no-go)
    
    // Parameter expansion
    vector[H]  beta_vec = beta[sub_ix];
    vector[H]  eta_vec  = eta[sub_ix];
        
    // Individial-level priors
    beta_pr ~ normal(0, 1);
    eta_pr  ~ normal(0, 1);
    
    for (i in 1:T) {
        
        // Compute likelihood of acting (go).
        p[:,i] = inv_logit( beta_vec .* (Q1 - Q2) );

        // Update action value (go).
        Q1 += eta_vec .* ( y[i] - Q1 );

        // Update action value (no-go).
        Q2 += eta_vec .* ( (1-y[i]) - Q2 ); 
        
    }
        
    // Likelihood
    to_array_1d(Y) ~ bernoulli( to_vector(p) );

}