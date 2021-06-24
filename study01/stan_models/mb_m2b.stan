data {

    // Metadata
    int<lower=1>  N;                   // Number of total stimuli
    int<lower=1>  M;                   // Number of total exposures
    int<lower=1>  J[N];                // Subject-indicator per stimulus
    
    // Response variables
    int  Y[M,N];                       // Action (Go = 1, No-Go = 0)
    
    // Task variables
    vector[N]  R[M];                   // Rewards (Reinforced = 1, Lessened = 0)
    vector[N]  W[M,3];                 // Instrumental learning bias
        
    // Mappings
    vector[N]  C[M];                   // Censored data (Observed = 1, Censored = 0)      
    
}
transformed data {
    
    // Indicator functions
    vector[N]  one_hot[M];
    for (m in 1:M) {
        for (n in 1:N) {
            one_hot[m,n] = Y[m,n];
        }
    }

}
parameters {
    
    // Group-level parameters
    vector[4] mu_pr;

    // Subject-level parameters
    matrix[4,max(J)]  theta_pr;
    
    // Subject-level covariance
    cholesky_factor_corr[4]  L;
    vector[4]  sigma_pr;

}
transformed parameters {

    // Subject-level parameters
    vector[max(J)]  b0;                // Choice sensitivity
    vector[max(J)]  b1;                // Go bias (all trials)
    vector[max(J)]  a1;                // Learning rate (go, rewarded)
    vector[max(J)]  a2;                // Learning rate (no-go, punished)
    vector[max(J)]  a3;                // Learning rate (all else)
    
    // Construction block
    {
    
    // Rotate random effects
    matrix[max(J),4] theta = transpose(rep_matrix(mu_pr, max(J)) + diag_pre_multiply(exp(sigma_pr), L) * theta_pr);
    
    // Extract random effects
    b0 = theta[,1] * 5;
    b1 = theta[,2] * 5;
    a1 = Phi_approx(theta[,3] + theta[,4]);
    a2 = Phi_approx(theta[,3] - theta[,4]);
    a3 = Phi_approx(theta[,3]);
    
    }

}
model {
       
    // Priors
    target += normal_lpdf(mu_pr | 0, 2.5);
    target += std_normal_lpdf(to_vector(theta_pr));
    target += std_normal_lpdf(to_vector(sigma_pr));
    target += lkj_corr_cholesky_lpdf(L | 1);
    
    // Likelihood block
    {
    
    // Parameter expansion
    vector[N]  b0_vec = b0[J];
    vector[N]  b1_vec = b1[J];
    vector[N]  a1_vec = a1[J];
    vector[N]  a2_vec = a2[J];
    vector[N]  a3_vec = a3[J];

    // Initialize Q-values
    vector[N]  Q1 = 0.5 * b0_vec;
    vector[N]  Q2 = 0.5 * b0_vec;
    
    // Construct predictor terms
    matrix[N,M] mu = rep_matrix(0, N, M);
    
    for (m in 1:M) {

        // Define bias
        vector[N] bias = b1_vec;

        // Precompute predictor
        mu[,m] = C[m] .* (Q1 - Q2 + bias);
        
        // Define learning rate
        vector[N] eta_vec = W[m,1] .* a1_vec + W[m,2] .* a2_vec + W[m,3] .* a3_vec;
        
        // Update Q-value (go)
        Q1 += one_hot[m] .* ( eta_vec .* ( b0_vec .* R[m] - Q1 ) );
        
        // Update action value (no-go)
        Q2 += (1-one_hot[m]) .* ( eta_vec .* ( b0_vec .* R[m] - Q2 ) );
    
    }
    
    // Likelihood
    target += bernoulli_logit_lpmf(to_array_1d(Y) | to_vector(mu));
    
    }
        
}