data {

    // Metadata
    int  H;                  // Number of subjects x robots 
    int  T;                  // Number of exposures
    
    // Data
    int        Y[T,H];       // Action (Go = 1, No-Go = 0)
    vector[H]  R[T];         // Rewards
    
    // Mappings
    int        sub_ix[H];    // Robot-to-subject mapping
    vector[H]  obs_ix[T];    // Trial      
    vector[H]  pav_ix;       // Robot-to-valence mapping      
    
}
transformed data {

    // Number of subjects
    int  N = max(sub_ix);
    
    // Indicator functions
    vector[H]  one_hot[T];   // Action (Go = 1, No-Go = 0)

    for (i in 1:T) {
        for (j in 1:H) {
            one_hot[i,j] = Y[i,j];
        }
    }

}
parameters {
    
    // Group-level parameters
    vector[2] mu_pr;
    
    // Group-level covariance
    cholesky_factor_corr[2]  L;
    vector[2]  sigma_pr;

    // Subject-level parameters
    matrix[2,N]  theta_pr;

}
transformed parameters {

    // Subject-level parameters
    vector[N]  beta;
    vector[N]  eta;
    
    // Construction block
    {
    
    // Rotate random effects
    matrix[2,N] theta = rep_matrix(mu_pr, N) + diag_pre_multiply( exp(sigma_pr), L ) * theta_pr;
    
    beta = theta[1]' * 5;
    eta  = Phi_approx( theta[2]' );
    
    }

}
model {
       
    // Priors
    mu_pr ~ normal(0, 2);
    L ~ lkj_corr_cholesky(2.0);
    sigma_pr ~ normal(0, 2);
    to_vector(theta_pr) ~ std_normal();
    
    // Likelihood block
    {
    
    // Parameter expansion
    vector[H]  beta_vec = beta[sub_ix];
    vector[H]  eta_vec = eta[sub_ix];
    
    // Generated quantities
    vector[H]  Q1 = rep_vector(0.5, H);
    vector[H]  Q2 = rep_vector(0.5, H);
    
    // Likelihood (all robots)
    for (i in 1:T) {
    
        // Compute action likelihood
        Y[i] ~ bernoulli_logit( obs_ix[i] .* beta_vec .* (Q1 - Q2) );
        
        // Update action value (go)
        Q1 += one_hot[i] .* ( eta_vec .* ( R[i] - Q1 ) );
        
        // Update action value (no-go)
        Q2 += (1-one_hot[i]) .* ( eta_vec .* ( R[i] - Q2 ) );
    
    }
    
    }
        
}