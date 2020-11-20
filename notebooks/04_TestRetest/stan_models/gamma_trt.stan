functions {

    // (Mode, SD)-paramterized Gamma distribution
    real gamma_mode_lpdf(vector z, vector mu, real sigma){
        vector[rows(mu)] beta = (mu + sqrt(square(mu) + 4*sigma^2)) / (2 * sigma^2);
        vector[rows(mu)] alpha = 1 + mu .* beta;
        return gamma_lpdf(z | alpha, beta);
    }

}
data {

    // Metadata
    int  N;
    int  K;
    int  T;
    int  J[2,N];
    
    // Data
    matrix[T,K]  X[2,N];
    vector[T]    Y[2,N];
    
}
parameters {
    
    // Group-level parameters (pre-transform)
    matrix[K,2]  mu_pr;
    
    // Subject-level parameters (pre-transform)
    matrix[K,N]  beta_c_pr;
    matrix[K,N]  beta_d_pr;
    
    // Parameter covariance
    vector[K]  sigma_c_pr;
    vector[K]  sigma_d_pr;
    
    // Noise
    // vector<lower=0>[N]  shape;

}
model {

    // Generated quantities
    matrix[K,N] beta[2];
    
    // Rotate random effects
    matrix[K,N] beta_c = diag_matrix( exp(sigma_c_pr) ) * beta_c_pr;
    matrix[K,N] beta_d = diag_matrix( exp(sigma_d_pr) ) * beta_d_pr;

    // Construct individual-level parameters
    beta[1] = rep_matrix(mu_pr[:,1], N) + beta_c - beta_d;
    beta[2] = rep_matrix(mu_pr[:,2], N) + beta_c + beta_d;
    
    // Priors
    mu_pr[1] ~ normal(0.75, 0.5);
    for (i in 2:K) { mu_pr[i] ~ normal(0, 0.5); }
    to_vector(beta_c_pr) ~ normal(0, 1);
    to_vector(beta_d_pr) ~ normal(0, 1);
    
    sigma_c_pr ~ normal(-2, 1);
    sigma_d_pr ~ normal(-2, 1);
    // shape ~ normal(0, 1);
    
    // Main loop
    for (i in 1:2) {
    
        for (j in 1:N) {
        
            Y[i,j,:J[i,j]] ~ student_t( 5, X[i,j,:J[i,j]] * beta[i,:,j], 0.5 );
        
        }
    
    }
    
}
generated quantities {
    
    // Test-retest parameters
    vector[K] sigma_c = exp(sigma_c_pr) .* exp(sigma_c_pr);
    vector[K] sigma_d = exp(sigma_d_pr) .* exp(sigma_d_pr);
    vector[K] rho = (sigma_c - sigma_d) ./ (sigma_c + sigma_d);

}