data {

    // Metadata
    int<lower=1>  N;                        // Number of total observations
    array[N] int<lower=1>  J;               // Subject-indicator per observation
    array[N] int<lower=1>  K;               // Bandit-indicator per observation
    array[N] int<lower=1, upper=2> M;       // Session-indicator per observation
    
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
    matrix[5,2]   theta_mu;                 // Population-level effects
    matrix[5,NJ]  theta_c_pr;               // Standardized subject-level effects (common)
    matrix[5,NJ]  theta_d_pr;               // Standardized subject-level effects (divergent)
    
    // Paramter variances
    matrix<lower=0>[5,2] sigma;             // Subject-level standard deviations

}
transformed parameters {

    array[2] vector[NJ]  b1;                // Inverse temperature
    array[2] vector[NJ]  b3;                // Go bias (positive valence)
    array[2] vector[NJ]  b4;                // Go bias (negative valence)
    array[2] vector[NJ]  a1;                // Learning rate (positive valence)
    array[2] vector[NJ]  a2;                // Learning rate (negative valence)

    // Construction block
    {
    
    // Rotate random effects
    matrix[NJ,5] theta_c = transpose(diag_pre_multiply(sigma[,1], theta_c_pr));
    matrix[NJ,5] theta_d = transpose(diag_pre_multiply(sigma[,2], theta_d_pr));
    
    // Construct random effects
    b1[1] = (theta_mu[1,1] + theta_c[,1] - theta_d[,1]) * 10;
    b1[2] = (theta_mu[1,2] + theta_c[,1] + theta_d[,1]) * 10;
    b3[1] = (theta_mu[2,1] + theta_c[,2] - theta_d[,2]) * 5;
    b3[2] = (theta_mu[2,2] + theta_c[,2] + theta_d[,2]) * 5;
    b4[1] = (theta_mu[3,1] + theta_c[,3] - theta_d[,3]) * 5;
    b4[2] = (theta_mu[3,2] + theta_c[,3] + theta_d[,3]) * 5;    
    a1[1] = Phi_approx(theta_mu[4,1] + theta_c[,4] - theta_d[,4]);
    a1[2] = Phi_approx(theta_mu[4,2] + theta_c[,4] + theta_d[,4]);
    a2[1] = Phi_approx(theta_mu[5,1] + theta_c[,5] - theta_d[,5]);
    a2[2] = Phi_approx(theta_mu[5,2] + theta_c[,5] + theta_d[,5]);
    
    }

}
model {

    // Initialize Q-values
    array[NJ, NK, 2, 2] real Q;
    Q[,,,1] = rep_array(0.5, NJ, NK, 2);
    Q[,,,2] = rep_array(0.5, NJ, NK, 2);

    // Construct linear predictor
    vector[N] mu;
    for (n in 1:N) {
    
        // Assign trial-level parameters
        real beta = b1[M[n],J[n]];
        real tau  = (V[n] == 1) ? b3[M[n],J[n]] : b4[M[n],J[n]];
        real eta  = (V[n] == 1) ? a1[M[n],J[n]] : a2[M[n],J[n]];
    
        // Compute (scaled) difference in expected values
        mu[n] = beta * (Q[J[n],K[n],M[n],2] - Q[J[n],K[n],M[n],1]) + tau;
        
        // Compute prediction error
        real delta = R[n] - Q[J[n],K[n],M[n],Y[n]+1];
        
        // Update state-action values
        Q[J[n],K[n],M[n],Y[n]+1] += eta * delta;
        
    }
    
    // Likelihood
    target += bernoulli_logit_lpmf(Y | mu); 
    
    // Priors
    target += normal_lpdf(to_vector(theta_mu) | 0, 2);
    target += std_normal_lpdf(to_vector(theta_c_pr));
    target += std_normal_lpdf(to_vector(theta_d_pr));
    target += student_t_lpdf(to_vector(sigma) | 3, 0, 1);

}
generated quantities {

    row_vector[2]  b1_mu = theta_mu[1] * 10;
    row_vector[2]  b3_mu = theta_mu[2] * 5;
    row_vector[2]  b4_mu = theta_mu[3] * 5;
    row_vector[2]  a1_mu = Phi_approx(theta_mu[4]);
    row_vector[2]  a2_mu = Phi_approx(theta_mu[5]);

}