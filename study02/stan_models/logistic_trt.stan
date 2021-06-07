data {

    // Metadata
    int  N;                         // Number of participants
    int  K;                         // Number of trialwise regressors
    int  T;                         // Number of trials
    
    // Data
    int            Y[N,2,T];
    matrix[T,K]    X[N,2];
    
}
parameters {
    
    // Group-level parameters
    matrix[K,2]  beta_mu;
    
    // Subject-level parameters (pre-transform)
    matrix[K,N]  beta_c_pr;
    matrix[K,N]  beta_d_pr;
    
    // Parameter covariance
    cholesky_factor_corr[K]  L_c;
    cholesky_factor_corr[K]  L_d;
    vector[K]  sigma_c_pr;
    vector[K]  sigma_d_pr;

}
model {
    
    // Rotate random effects
    matrix[K,N]  beta_c = diag_pre_multiply( exp(sigma_c_pr), L_c ) * beta_c_pr;
    matrix[K,N]  beta_d = diag_pre_multiply( exp(sigma_d_pr), L_d ) * beta_d_pr;

    // Construct subject-level parameters
    vector[K]  beta[2,N];
    
    for (i in 1:N) {
        beta[1,i] = beta_mu[:,1] + beta_c[:,i] - beta_d[:,i];
        beta[2,i] = beta_mu[:,2] + beta_c[:,i] + beta_d[:,i];
    }
    
    // Priors
    to_vector(beta_mu) ~ normal(0, 2);
    to_vector(beta_c_pr) ~ normal(0, 1);
    to_vector(beta_d_pr) ~ normal(0, 1);
    L_c ~ lkj_corr_cholesky(2.0);
    L_d ~ lkj_corr_cholesky(2.0);
    sigma_c_pr ~ normal(0, 1);
    sigma_d_pr ~ normal(0, 1);
    
    // Main loop
    for (i in 1:N) {
    
        for (j in 1:2) {
        
            Y[i,j] ~ bernoulli_logit( X[i,j] * beta[j,i] );
        
        }
    
    }
    
        
}
generated quantities {
    
    // Test-retest parameters
    vector[K] sigma_c = exp(sigma_c_pr) .* exp(sigma_c_pr);
    vector[K] sigma_d = exp(sigma_d_pr) .* exp(sigma_d_pr);
    vector[K] rho = (sigma_c - sigma_d) ./ (sigma_c + sigma_d);

}