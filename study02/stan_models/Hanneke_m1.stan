data {

    // Metadata
    int<lower=1>  N;                   // Number of total stimuli
    int<lower=1>  M;                   // Number of total exposures
    int<lower=1>  S[N];                // Subject-indicator per stimulus
    
    // Response 
    int  Y[M,N];                       // Action (Go = 1, No-Go = 0)
    
    // Reward
    vector[N]  R[M];                   // Rewards (Reinforced = 1, Lessened = 0)
        
}//data

transformed data {
    
    // reformat Y
    vector[N]  Y_vec[M];
    
    for (m in 1:M) {
        for (n in 1:N) {
            Y_vec[m, n] = Y[m,n];
        }//for
    }//for

}//transformed data


parameters {
    
    // A 2 parameters model
    
    vector[2] mu_pr;                   // Group-level parameters
    matrix[2, max(S)]  theta_pr;       // Subject-level parameters
    cholesky_factor_corr[2]  L;        // Subject-level covariance
    vector[2]  sigma_pr;               // Subject-level variance

}//params

transformed parameters {

    // Subject-level parameters
    vector[max(S)]  rho;               // Choice sensitivity
    vector[max(S)]  a;                 // Learning rate
    
    // Construction block
    {
    
    // Rotate random effects
    matrix[max(S),2] theta = transpose(rep_matrix(mu_pr, max(S)) + diag_pre_multiply(exp(sigma_pr), L) * theta_pr);
    
    // Extract random effects
    rho = theta[,1] * 5;
    a = Phi_approx(theta[,2]);
    
    }//Construction

}//transformed parameters

model {

     // Priors
    
    target += normal_lpdf(mu_pr | 0, 2.5);
    target += std_normal_lpdf(to_vector(theta_pr));
    target += std_normal_lpdf(to_vector(sigma_pr));
    target += lkj_corr_cholesky_lpdf(L | 1);

    {
    // reformat params
    vector[N]  rho_vec = rho[S];
    vector[N]  a_vec = a[S];
    
    // Initialize Q-values

    vector[N]  Q1 = 0.5 * rho_vec;
    vector[N]  Q2 = 0.5 * rho_vec;
    
    // Construct predictor terms
    matrix[N, M] mu = rep_matrix(0, N, M);
    
    // Iterate exposures (M)
    for (m in 1:M) {


        mu[,m] = (Q1 - Q2);
        
        // Update Q-value
        
        // Update  action value (go)
        Q1 += Y_vec[m] .* ( a_vec .* ( rho_vec .* R[m] - Q1 ) );
        
        // Update action value (no-go)
        Q2 += (1-Y_vec[m]) .* ( a_vec .* ( rho_vec .* R[m] - Q2 ) );
    

      
    
    }//for
    
    // Likelihood
    target += bernoulli_logit_lpmf(to_array_1d(Y) | to_vector(mu));
   }//ll

}//model