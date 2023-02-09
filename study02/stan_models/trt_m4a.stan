// Pavlovian bias + Go bias + valance eta
// implicit covariance matrix
data {

    // metadata
    int<lower=1>  N;                   // Number of observations
    int<lower=1>  E;                   // Number of total exposures
    int<lower=1>  S[N];                // Subject id (per observation)
    int<lower=1, upper=3> M[N];        // group-indicator (per observation)
    
    
    // response 
    int  Y[E, N];                      // Action (Go = 1, No-Go = 0)
    
    // outcome
    vector[N] R[E];                    // Rewards (Reinforced = 1, Lessened = 0)
    
    // remove low RT & null choices
    vector[N] C[E];                    // Choice (Observed = 1, Censored = 0)      
    
    // keep only good trials
    vector[N] V[E];                    // Valence (Win = 1, Lose = 0)
    
        
}//data

transformed data {
    
    int  NS = max(S);                       // Number of total subjects
   
}
parameters {
    
    
    // Subject-level parameters
    matrix[5,2]   mu_pr;        // Population-level effects
    matrix[5,NS]  theta_c_pr;   // Standardized subject-level effects (common)
    matrix[5,NS]  theta_d_pr;   // Standardized subject-level effects (divergent)

    // Paramter variances
    matrix<lower=0>[6,2] sigma;     // Subject-level standard deviations

}
transformed parameters {

    // Subject-level parameters
    vector[NS]  eta_gain[2];            // Learning rate gain
    vector[NS]  eta_loss[2];            // Learning rate gain
    vector[NS]  beta[2];                // Choice sensitivity (Inverse tmp)
    vector[NS]  beta_P[2];              // Pavlovian bias
    vector[NS]  beta_GO[2];             // GO bias
    
    // Construction block
    {
    
    // Rotate random effects
    matrix[NS,5] theta_c = transpose(diag_pre_multiply(sigma[,1], theta_c_pr));
    matrix[NS,5] theta_d = transpose(diag_pre_multiply(sigma[,1], theta_d_pr));

    
    // Construct individual-level parameters (session 1)
    eta_gain[1] = Phi_approx(mu_pr[1,1] + theta_c[,1] - theta_d[,1]);
    eta_loss[1] = Phi_approx(mu_pr[2,1] + theta_c[,2] + theta_d[,2]);
    beta[1] = (mu_pr[3,1] + theta_c[,3] - theta_d[,3]) * 5;
    beta_P[1] = (mu_pr[4,1] + theta_c[,4] - theta_d[,4]) * 5;
    beta_GO[1] = (mu_pr[5,1] + theta_c[,5] - theta_d[,5]) * 5;
 
    
    // Construct individual-level parameters (session 2)
    eta_gain[2] = Phi_approx(mu_pr[1,2] + theta_c[,1] - theta_d[,1]);
    eta_loss[2] = Phi_approx(mu_pr[2,2] + theta_c[,2] + theta_d[,2]);
    beta[2] = (mu_pr[3,2] + theta_c[,3] - theta_d[,3]) * 5;
    beta_P[2] = (mu_pr[4,2] + theta_c[,4] - theta_d[,4]) * 5;
    beta_GO[2] = (mu_pr[5,2] + theta_c[,5] - theta_d[,5]) * 5;

    
    
    }

}
model {
       
    
    // Initialize Q-values
    real Q[NS, E, 2]; // NS, E, SESSION, CHOICE
    
    Q[,,1] = to_array_2d(rep_matrix(beta[1]*.5, E));
    Q[,,2] = to_array_2d(rep_matrix(beta[2]*.5, E));

    
    
    // Construct linear predictor
    matrix[N, E] mu = rep_matrix(0, N, E);
    
    // Main loop


    // Iterate exposures (E)
    for (e in 1:E) {
        for (n in 1:N) {
    
        // Define bias
        real bias =  beta_GO[M[n], S[n]] + (V[e, n] * beta_P[M[n], S[n]]);

        // Define eta
        real eta = (V[e, n] * eta_gain[M[n], S[n]]) + ((1-V[e, n]) * eta_loss[M[n], S[n]]);


        // Compute (scaled) difference in expected values
        mu[n, e] = C[e, n] .* (Q[S[n], e, M[n]] - 0.5 + bias);


        // Compute prediction error
        real delta = beta[M[n], S[n]] * R[e, n] - Q[S[n], e, M[n]];


        // Update state-action values
        Q[S[n], e, M[n]] += eta .* delta;
        }
        
        
    }
    // Likelihood
    target += bernoulli_logit_lpmf(to_array_1d(Y) | to_vector(mu)); 
      
     
    
    // Priors
    target += normal_lpdf(to_vector(mu_pr) | 0, 2);
    target += std_normal_lpdf(to_vector(theta_c_pr));
    target += std_normal_lpdf(to_vector(theta_d_pr));
    target += student_t_lpdf(to_vector(sigma) | 3, 0, 1);
    
    
    
    }
        
