//Pavlovian bias + Go bias
data {

    // metadata
    int<lower=1>  N;                   // Number of observations
    int<lower=1>  E;                   // Number of total Exposures
    int<lower=1>  S[N];                // Subject id (per stimulus)
    
    // response 
    int  Y[E, N];                       // Action (Go = 1, No-Go = 0)

    
    
    // outcome
    array[E] vector[N] R;                   // Rewards (Reinforced = 1, Lessened = 0)
    
    // remove low RT & null choices
    array[E] vector[N] C;                   // (Observed = 1, Censored = 0)      
    
    // keep only good trials
    array[E] vector[N] V;                   // Valence (Win = 1, Lose = 0)
   
   
        
}//data
transformed data {
    
    array[E] vector[N] Y_mat;                // Action (Go = 1, No-Go = 0)

    for (e in 1:E) {
        for (n in 1:N) {
            Y_mat[e,n] = Y[e,n];
        }
    }

}

parameters {
    
    // A 4 parameters model
    
    vector[4] mu_pr;                   // Group-level parameters
    vector[4] sigma_pr;               // Group-level variance

    matrix[4, max(S)]  theta_pr;       // Subject-level parameters
    cholesky_factor_corr[4]  L;        // Subject-level covariance

}//params

transformed parameters {

    // Subject-level parameters
    vector[max(S)]  eta;                 // Learning rate
    vector[max(S)]  beta;                // Choice sensitivity (Inverse tmp)
    vector[max(S)]  beta_P;              // Pavlovian bias
    vector[max(S)]  beta_GO;             // GO bias


    
    // Construction block
    {
    
    // Rotate random effects
    matrix[max(S),4] theta = transpose(rep_matrix(mu_pr, max(S)) + diag_pre_multiply(exp(sigma_pr), L) * theta_pr);
    
    // Extract random effects
    eta = Phi_approx(theta[,1]);
    beta = theta[,2] * 5;
    beta_P = theta[,3] * 5;
    beta_GO = theta[,4] * 5;

    
    }//Construction

}//transformed parameters

model {

     // Priors
    
    target += normal_lpdf(mu_pr | 0, 2.5);
    target += std_normal_lpdf(to_vector(theta_pr));
    target += std_normal_lpdf(to_vector(sigma_pr));
    target += lkj_corr_cholesky_lpdf(L | 1);

    {
    // reformat params (per subject id)
    vector[N]  eta_i = eta[S];
    vector[N]  beta_i = beta[S];
    vector[N]  beta_P_i = beta_P[S];
    vector[N]  beta_GO_i = beta_GO[S];
    
    
    // Initialize Q-values
    vector[N]  Q1 = 0.5 * beta_i;
    vector[N]  Q2 = 0.5 * beta_i;
    
    // Construct predictor terms
    matrix[N, E] mu = rep_matrix(0, N, E);
    
    // Iterate exposures (E)
    for (e in 1:E) {

        // Define bias
        vector[N] bias =  beta_GO_i + (V[e] .* beta_P_i);
        
        //choice 
        mu[,e] = C[e] .* (Q1 - Q2 + bias);
        
        // Update Q-value
        
        Q1 +=  Y_mat[e] .* (eta_i .* ( beta_i .* R[e] - Q1 )) ;
        Q2 +=  (1-Y_mat[e]) .* (eta_i .* ( beta_i .* R[e] - Q2 )) ;
        
       
    
    }//for
    
    // Likelihood
    target += bernoulli_logit_lpmf(to_array_1d(Y) | to_vector(mu));
   }//ll

}//model