data {

    // Metadata
    int<lower=1>  N;                        // Number of total observations
    array[N] int<lower=1>  J;               // Subject-indicator per observation
    array[N] int<lower=1>  K;               // Bandit-indicator per observation
    
    // Data
    array[N] int<lower=0, upper=1>  Y;      // Response (go = 1, no-go = 0)
    array[N] int<lower=0, upper=1>  R;      // Outcome (better = 1, worse = 0)
    array[N] int<lower=0, upper=1>  V;      // Valence (positive = 1, negative = 0)

}
transformed data {

    int  NJ = max(J);                       // Number of total subjects
    int  NK = max(K);                       // Number of total bandits

}
parameters {

    // Participant parameters
    vector[4]     theta_mu;                 // Population-level effects
    matrix[4,NJ]  theta_pr;                 // Standardized subject-level effects
    
    // Paramter variances
    vector<lower=0>[4] sigma;               // Subject-level standard deviations

}
transformed parameters {

    vector[NJ]  b1;                         // Inverse temperature
    vector[NJ]  b2;                         // Go bias
    vector[NJ]  b3;                         // Pavlovian bias
    vector[NJ]  a1;                         // Learning rate

    // Construction block
    {
    
    // Rotate random effects
    matrix[NJ,4] theta = transpose(diag_pre_multiply(sigma, theta_pr));
    
    // Construct random effects
    b1 = (theta_mu[1] + theta[,1]) * 10;
    b2 = (theta_mu[2] + theta[,2]) * 5;
    b3 = (theta_mu[3] + theta[,3]) * 5;
    a1 = Phi_approx(theta_mu[4] + theta[,4]);
    
    }

}
model {

    // Initialize Q-values
    array[NJ, NK, 2] real Q = rep_array(0.5, NJ, NK, 2);

    // Construct linear predictor
    vector[N] mu;
    for (n in 1:N) {
    
        // Compute (scaled) difference in expected values
        mu[n] = b1[J[n]] * (Q[J[n],K[n],2] - Q[J[n],K[n],1]) + b2[J[n]] + b3[J[n]] * V[n];
        
        // Compute prediction error
        real delta = R[n] - Q[J[n],K[n],Y[n]+1];
        
        // Assign learning rate
        real eta = a1[J[n]];
        
        // Update state-action values
        Q[J[n],K[n],Y[n]+1] += eta * delta;
        
    }
    
    // Likelihood
    target += bernoulli_logit_lpmf(Y | mu); 
    
    // Priors
    target += normal_lpdf(theta_mu | 0, 2);
    target += std_normal_lpdf(to_vector(theta_pr));
    target += student_t_lpdf(sigma | 3, 0, 1);

}