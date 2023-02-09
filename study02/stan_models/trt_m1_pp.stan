data {

    // Metadata
    int  H;                    // Number of subjects x robots 
    int  T;                    // Number of exposures
    
    // Data
    int        Y[2,T,H];       // Action (Go = 1, No-Go = 0)
    vector[H]  R[2,T];         // Rewards
    
    // Mappings
    int        sub_ix[H];      // Robot-to-subject mapping
    vector[H]  pav_ix;         // Robot-to-valence mapping      
    vector[H]  obs_ix[2,T];    // Trial      
    
}
transformed data {

    // Number of subjects
    int  N = max(sub_ix);
    
    // Indicator functions
    vector[H]  one_hot[2,T]; // Action (Go = 1, No-Go = 0)

    for (i in 1:2) {
        for (j in 1:T) {
            one_hot[i,j] = to_vector(Y[i,j]);
        }
    }

}
parameters {
    
    // Group-level parameters
    matrix[4,2]  mu_pr;
    
    // Group-level covariance
    cholesky_factor_corr[4]  L_c;
    cholesky_factor_corr[4]  L_d;
    vector[4]  sigma_c_pr;
    vector[4]  sigma_d_pr;
    
    // Subject-level parameters
    matrix[4,N]  theta_c_pr;
    matrix[4,N]  theta_d_pr;

}
transformed parameters {

    // Subject-level parameters
    vector[N]  beta[2];
    vector[N]  eta[2];
    vector[N]  tau[2];
    vector[N]  nu[2];
    
    // Construction block
    {
    
    // Rotate random effects
    matrix[4,N]  theta_c = diag_pre_multiply( exp(sigma_c_pr), L_c ) * theta_c_pr;
    matrix[4,N]  theta_d = diag_pre_multiply( exp(sigma_d_pr), L_d ) * theta_d_pr;
    
    // Construct individual-level parameters (session 1)
    beta[1] = (mu_pr[1,1] + theta_c[1,:]' - theta_d[1,:]') * 5;
    eta[1]  = Phi_approx( mu_pr[2,1] + theta_c[2,:]' - theta_d[2,:]' );
    tau[1]  = mu_pr[3,1] + theta_c[3,:]' - theta_d[3,:]';
    nu[1]   = mu_pr[4,1] + theta_c[4,:]' - theta_d[4,:]';
    
    // Construct individual-level parameters (session 2)
    beta[2] = (mu_pr[1,2] + theta_c[1,:]' + theta_d[1,:]') * 5;
    eta[2]  = Phi_approx( mu_pr[2,2] + theta_c[2,:]' + theta_d[2,:]' );
    tau[2]  = mu_pr[3,2] + theta_c[3,:]' + theta_d[3,:]';
    nu[2]   = mu_pr[4,2] + theta_c[4,:]' + theta_d[4,:]';
    
    }

}
model {
       
    // Priors
    to_vector(mu_pr) ~ normal(0, 2);
    L_c ~ lkj_corr_cholesky(2.0);
    L_d ~ lkj_corr_cholesky(2.0);
    sigma_c_pr ~ normal(0, 1);
    sigma_d_pr ~ normal(0, 1);
    to_vector(theta_c_pr) ~ std_normal();
    to_vector(theta_d_pr) ~ std_normal();
    
    // Main loop
    for (i in 1:2) {
    
        // Parameter expansion
        vector[H]  beta_vec = beta[i][sub_ix];
        vector[H]  eta_vec = eta[i][sub_ix];
        vector[H]  tau_vec = tau[i][sub_ix];
        vector[H]  nu_vec = nu[i][sub_ix];
    
        // Generated quantities
        vector[H]  Q1 = rep_vector(0.5, H);
        vector[H]  Q2 = rep_vector(0.5, H);
        
        // Likelihood (all robots)
        for (j in 1:T) {

            // Compute action likelihood
            Y[i,j] ~ bernoulli_logit( obs_ix[i,j] .* beta_vec .* (Q1 - Q2 + tau_vec + nu_vec .* pav_ix) );

            // Update action value (go)
            Q1 += one_hot[i,j] .* ( eta_vec .* ( R[i,j] - Q1 ) );

            // Update action value (no-go)
            Q2 += (1-one_hot[i,j]) .* ( eta_vec .* ( R[i,j] - Q2 ) );

        }
    
    }
        
}
generated quantities {
    
    // Test-retest parameters
    vector[4] sigma_c = exp(sigma_c_pr) .* exp(sigma_c_pr);
    vector[4] sigma_d = exp(sigma_d_pr) .* exp(sigma_d_pr);
    vector[4] rho = (sigma_c - sigma_d) ./ (sigma_c + sigma_d);

}