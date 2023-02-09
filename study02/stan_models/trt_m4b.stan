//Pavlovian bias + Go bias + valance eta
data {

    // metadata
    int<lower=1>  N;                   // Number of observations
    int<lower=1>  E;                   // Number of total Exposures
    int<lower=1>  S[N];                // Subject id (per stimulus)
    
    // response 
    int  Y[2, E, N];                   // Action (Go = 1, No-Go = 0)
    
    // outcome
    vector[N] R[2,E];                  // Rewards (Reinforced = 1, Lessened = 0)
    
    // remove low RT & null choices
    vector[N] C[2,E];                  // (Observed = 1, Censored = 0)      
    
    // keep only good trials
    vector[N] V[2,E];                 // Valence (Win = 1, Lose = 0)
    
        
}//data

transformed data {
    
    //real Y_mat[2, E, N];  
    vector[N] Y_mat[2,E];
    
    for (i in 1:2) {
        for (n in 1:N) {
            Y_mat[i,,n] = Y[i,,n];
        }
    }
    
    // A 5 parameters model
    int n_params = 4;
    

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
    matrix[4,max(S)]  theta_c_pr;
    matrix[4,max(S)]  theta_d_pr;

}
transformed parameters {

    // Subject-level parameters
    vector[max(S)]  eta_gain[2];            // Learning rate gain
    vector[max(S)]  eta_loss[2];            // Learning rate gain
    vector[max(S)]  beta[2];                // Choice sensitivity (Inverse tmp)
    vector[max(S)]  beta_P[2];              // Pavlovian bias
    
    // Construction block
    {
    
    // Rotate random effects
    matrix[4,max(S)]  theta_c = diag_pre_multiply( exp(sigma_c_pr), L_c ) * theta_c_pr;
    matrix[4,max(S)]  theta_d = diag_pre_multiply( exp(sigma_d_pr), L_d ) * theta_d_pr;
    
    // Construct individual-level parameters (session 1)
    eta_gain[1] = Phi_approx(mu_pr[1,1] + theta_c[1,:]' - theta_d[1,:]');
    eta_loss[1] = Phi_approx(mu_pr[2,1] + theta_c[2,:]' - theta_d[2,:]');
    beta[1] = (mu_pr[3,1] + theta_c[3,:]' - theta_d[3,:]') * 5;
    beta_P[1] = (mu_pr[4,1] + theta_c[4,:]' - theta_d[4,:]') * 5;
    
    // Construct individual-level parameters (session 2)
    eta_gain[2] = Phi_approx(mu_pr[1,2] + theta_c[1,:]' - theta_d[1,:]');
    eta_loss[2] = Phi_approx(mu_pr[2,2] + theta_c[2,:]' - theta_d[2,:]');
    beta[2] = (mu_pr[3,2] + theta_c[3,:]' - theta_d[3,:]') * 5;
    beta_P[2] = (mu_pr[4,2] + theta_c[4,:]' - theta_d[4,:]') * 5;
    
    
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
        vector[N]  eta_gain_i = eta_gain[i][S];
        vector[N]  eta_loss_i = eta_loss[i][S];
        vector[N]  beta_i = beta[i][S];
        vector[N]  beta_P_i = beta_P[i][S];
    
       
        // Initialize Q-values
        vector[N]  Q1 = 0.5 * beta_i;
        vector[N]  Q2 = 0.5 * beta_i;
        
        
        
        // Construct predictor terms
        matrix[N, E] mu = rep_matrix(0, N, E);
    
        // Iterate exposures (E)
        for (e in 1:E) {
        
            
            // Define bias
            vector[N] bias =  V[i, e] .* beta_P_i;

            // Define eta
            vector[N] eta_i = (V[i, e] .* eta_gain_i) + ((1-V[i, e]) .*eta_loss_i);
            
        
            // Compute action likelihood
            Y[i,e,] ~ bernoulli_logit( C[i, e] .* (Q1 - Q2 + bias));


            // Update action value 
            Q1 +=  Y_mat[i,e] .* (eta_i .* ( beta_i .* R[i,e] - Q1 )) ;
            Q2 +=  (1-Y_mat[i,e]) .* (eta_i .* ( beta_i .* R[i,e] - Q2 )) ;
     

        }
    
    }
        
}
generated quantities {
    
    // Test-retest parameters
    vector[4] sigma_c = exp(sigma_c_pr) .* exp(sigma_c_pr);
    vector[4] sigma_d = exp(sigma_d_pr) .* exp(sigma_d_pr);
    vector[4] rho = (sigma_c - sigma_d) ./ (sigma_c + sigma_d);

}