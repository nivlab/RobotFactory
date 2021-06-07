data {

    // Metadata
    int  N;                         // Number of participants
    int  T;                         // Number of trials
    
    // Data
    matrix[T,4]  X[N,2];
    int          Y[N,2,T];          // Choices (Go = 1, No-Go = 0)
    
}
parameters {
    
    // Coefficients
    vector[4]  beta_mu_pr[2];
    vector[4]  beta_c_pr[N];
    vector[4]  beta_d_pr[N];
    
    // Variances
    vector<lower=0>[4] sigma_c;
    vector<lower=0>[4] sigma_d;

}
transformed parameters {

    vector[4]  beta[N,2];
    
    for (i in 1:N) {
    
        // Session 1
        beta[i,1] = beta_mu_pr[1] + sigma_c .* beta_c_pr[i] - sigma_d .* beta_d_pr[i];

        // Session 2
        beta[i,2] = beta_mu_pr[2] + sigma_c .* beta_c_pr[i] + sigma_d .* beta_d_pr[i];
    
    }
    
}
model {
    
    // Group-level priors
    for (i in 1:2) { beta_mu_pr[i] ~ normal(0, 1); }
    sigma_c ~ normal(0, 2);
    sigma_d ~ normal(0, 2);
    
    // Individual-level priors
    for (i in 1:N) {
        beta_c_pr[i] ~ normal(0, 1);
        beta_d_pr[i] ~ normal(0, 1);
    }
    
    for (i in 1:N) {
    
        for (j in 1:2) {
        
            Y[i,j] ~ bernoulli_logit( X[i,j] * beta[i,j] );
        
        }
        
    }
    
    
        
}
generated quantities {
    
    // Test-retest parameters
    vector[4] rho;
    for (i in 1:4) {
        rho[i] = (sigma_c[i]^2 - sigma_d[i]^2) / (sigma_c[i]^2 + sigma_d[i]^2);
    }

}