//Pavlovian bias + Go bias + valance eta
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
    
    // congruence by set up
    array[E] vector[N] CONTEXT_CONG;        // congruence (GW, NGAL = 1, NGW, GAL = 0)
    

        
        
}//data

transformed data {
    
    array[E] vector[N] Y_mat;                // Action (Go = 1, No-Go = 0)

    for (e in 1:E) {
        for (n in 1:N) {
            Y_mat[e,n] = Y[e,n];
        }
    }
    
    // A 5 parameters model
    int n_params = 5;

}

parameters {
    
    vector[n_params] mu_pr;                   // Group-level parameters
    vector[n_params] sigma_pr;               // Group-level variance

    matrix[n_params, max(S)]  theta_pr;       // Subject-level parameters
    cholesky_factor_corr[n_params]  L;        // Subject-level covariance

}//params

transformed parameters {

    // Subject-level parameters
    vector[max(S)]  eta_cong;            // Learning rate congruent set up
    vector[max(S)]  eta_incong;          // Learning rate incongruent set up
    vector[max(S)]  beta;                // Choice sensitivity (Inverse tmp)
    vector[max(S)]  beta_P;              // Pavlovian bias
    vector[max(S)]  beta_GO;             // GO bias


    
    // Construction block
    {
    
    // Rotate random effects
    matrix[max(S),n_params] theta = transpose(rep_matrix(mu_pr, max(S)) + diag_pre_multiply(exp(sigma_pr), L) * theta_pr);
    
    // Extract random effects
    eta_cong = Phi_approx(theta[,1]);
    eta_incong = Phi_approx(theta[,2]);
    beta = theta[,3] * 5;
    beta_P = theta[,4] * 5;
    beta_GO = theta[,5] * 5;

    
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
    vector[N]  eta_cong_i = eta_cong[S];
    vector[N]  eta_incong_i = eta_incong[S];
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
        
        // Define eta
        vector[N] eta_i = (CONTEXT_CONG[e] .* eta_cong_i) + ((1-CONTEXT_CONG[e]) .*eta_incong_i);
        
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