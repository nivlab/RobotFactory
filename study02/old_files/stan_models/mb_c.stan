data {

    // Metadata
    int<lower=1>  N;                   // Number of total stimuli
    int<lower=1>  M;                   // Number of total exposures
    int<lower=1>  J[N];                // Subject-indicator per stimulus
    
    // Data
    int  Y[2,M,N];                     // Action (Go = 1, No-Go = 0)
    
    // Task variables
    vector[N]  R[2,M];                 // Rewards (Reinforced = 1, Punished = 0)
    vector[N]  V[2,M];                 // Valence (Win = 1, Lose = 0)
    vector[N]  W[2,M,3];               // Instrumental learning bias
        
    // Mappings
    vector[N]  C[2,M];                 // Censored data (Observed = 1, Censored = 0)
    
}
transformed data {
    
    // Indicator functions
    vector[N]  one_hot[2,M];
    for (k in 1:2) {
        for (m in 1:M) {
            one_hot[k,m] = to_vector(Y[k,m]);
        }
    }

}
parameters {
    
    // Group-level parameters
    matrix[5,2]  mu_pr;

    // Subject-level parameters
    matrix[5,max(J)]  theta_c_pr;      // Between-subject effects
    matrix[5,max(J)]  theta_d_pr;      // Within-subject effects
    
    // Subject-level covariance
    cholesky_factor_corr[5] L_c;       // Cholesky factor of correlation matrix
    cholesky_factor_corr[5] L_d;       // Cholesky factor of correlation matrix
    matrix[5,2] sigma_pr;              // Subject-level standard deviations

}
transformed parameters {

    // Subject-level parameters
    vector[max(J)]  b0[2];             // Choice sensitivity
    vector[max(J)]  b1[2];             // Go bias (win trials)
    vector[max(J)]  b2[2];             // Go bias (lose trials)
    vector[max(J)]  a1[2];             // Learning rate (go, rewarded)
    vector[max(J)]  a2[2];             // Learning rate (no-go, punished)
    vector[max(J)]  a3[2];             // Learning rate (all else)
    
    // Construction block
    {
    
    // Rotate random effects
    matrix[max(J),5] theta_c = transpose(diag_pre_multiply(exp(sigma_pr[,1]), L_c) * theta_c_pr);
    matrix[max(J),5] theta_d = transpose(diag_pre_multiply(exp(sigma_pr[,2]), L_d) * theta_d_pr);
    
    // Construct random effects (first half)
    b0[1] = ((mu_pr[1,1] + theta_c[,1] - theta_d[,1])) * 5;
    b1[1] = ((mu_pr[2,1] + theta_c[,2] - theta_d[,2])
           - (mu_pr[3,1] + theta_c[,3] - theta_d[,3])) * 5;    
    b2[1] = ((mu_pr[2,1] + theta_c[,2] - theta_d[,2])
           + (mu_pr[3,1] + theta_c[,3] - theta_d[,3])) * 5;    
    a1[1] = Phi_approx((mu_pr[4,1] + theta_c[,4] - theta_d[,4])
                     + (mu_pr[5,1] + theta_c[,5] - theta_d[,5]));
    a2[1] = Phi_approx((mu_pr[4,1] + theta_c[,4] - theta_d[,4])
                     - (mu_pr[5,1] + theta_c[,5] - theta_d[,5]));
    a3[1] = Phi_approx((mu_pr[4,1] + theta_c[,4] - theta_d[,4]));
    
    // Construct random effects (second half)
    b0[2] = ((mu_pr[1,2] + theta_c[,1] + theta_d[,1])) * 5;
    b1[2] = ((mu_pr[2,2] + theta_c[,2] + theta_d[,2])
           - (mu_pr[3,2] + theta_c[,3] + theta_d[,3])) * 5;    
    b2[2] = ((mu_pr[2,2] + theta_c[,2] + theta_d[,2])
           + (mu_pr[3,2] + theta_c[,3] + theta_d[,3])) * 5;    
    a1[2] = Phi_approx((mu_pr[4,2] + theta_c[,4] + theta_d[,4])
                     + (mu_pr[5,2] + theta_c[,5] + theta_d[,5]));
    a2[2] = Phi_approx((mu_pr[4,2] + theta_c[,4] + theta_d[,4])
                     - (mu_pr[5,2] + theta_c[,5] + theta_d[,5]));
    a3[2] = Phi_approx((mu_pr[4,2] + theta_c[,4] + theta_d[,4]));
    
    }

}
model {
       
    // Priors
    target += normal_lpdf(to_vector(mu_pr) | 0, 2.5);
    target += std_normal_lpdf(to_vector(theta_c_pr));
    target += std_normal_lpdf(to_vector(theta_d_pr));
    target += std_normal_lpdf(to_vector(sigma_pr));
    target += lkj_corr_cholesky_lpdf(L_c | 1);
    target += lkj_corr_cholesky_lpdf(L_d | 1);
    
    // Main loop
    for (k in 1:2) {

        // Parameter expansion
        vector[N]  b0_vec = b0[k,J];
        vector[N]  b1_vec = b1[k,J];
        vector[N]  b2_vec = b2[k,J];
        vector[N]  a1_vec = a1[k,J];
        vector[N]  a2_vec = a2[k,J];
        vector[N]  a3_vec = a3[k,J];

        // Initialize Q-values
        vector[N]  Q1 = 0.5 * b0_vec;
        vector[N]  Q2 = 0.5 * b0_vec;

        // Construct predictor terms
        matrix[N,M] mu = rep_matrix(0, N, M);

        for (m in 1:M) {

            // Define bias
            vector[N] bias = b1_vec + V[k,m] .* b2_vec;

            // Precompute predictor
            mu[,m] = C[k,m] .* (Q1 - Q2 + bias);

            // Define learning rate
            vector[N] eta_vec = W[k,m,1] .* a1_vec + W[k,m,2] .* a2_vec + W[k,m,3] .* a3_vec;

            // Update Q-value (go)
            Q1 += one_hot[k,m] .* ( eta_vec .* ( b0_vec .* R[k,m] - Q1 ) );

            // Update action value (no-go)
            Q2 += (1-one_hot[k,m]) .* ( eta_vec .* ( b0_vec .* R[k,m] - Q2 ) );

        }

        // Likelihood
        target += bernoulli_logit_lpmf(to_array_1d(Y[k]) | to_vector(mu));
    
    }

}
generated quantities {
    
    // Intra-class correlations
    vector[5] sigma_c = rows_dot_self(exp(sigma_pr[,1]));
    vector[5] sigma_d = rows_dot_self(exp(sigma_pr[,2]));
    vector[5] rho = (sigma_c - sigma_d) ./ (sigma_c + sigma_d);

}