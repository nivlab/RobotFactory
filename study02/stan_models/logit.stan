data {

    // Metadata
    int<lower=1>  N;                        // Number of total observations
    int<lower=1>  M1;                       // Number of within-participant predictors
    int<lower=1>  M2;                       // Number of between-participant predictors
    array[N] int<lower=1>  J;               // Participant-indicator per observation
    array[N] int<lower=1>  K;               // Session-indicator per observation
    
    // Data
    array[N] int<lower=0, upper=1>  Y;      // Response (go = 1, no-go = 0)
    
    // Design matrix
    array[N] row_vector[M1]  X1;            // Within-participant predictors
    array[N] row_vector[M2]  X2;            // Between-participant predictors

}
transformed data {

    int  NJ = max(J);                       // Total number of participants
    int  NK = max(K);                       // Total number of sessions

}
parameters {

    // Population-level effects
    vector[M1]  beta_mu_01;                 // Within-participant effects (grand means)
    vector[M2]  beta_mu_02;                 // Between-participant effects (grand means)

    // Group-level effects
    matrix[NK-1,M1] beta_pr_1;              // Level-1 effects (sessions)
    matrix[NJ,M1]   beta_pr_2;              // Level-2 effects (participants)
        
    // Variances
    vector<lower=0>[M1] sigma_1;            // Level-1 variability (sessions)
    vector<lower=0>[M1] sigma_2;            // Level-2 variability (participants)
    
}
transformed parameters {

    array[NJ,NK] vector[M1] beta;           // Within-participant effects (participants)
    
    for (m in 1:M1) {
    
        // Compute level-1 coefficients (sum-to-zero constraint)
        vector[NK] beta_1 = append_row(sigma_1[m] * beta_pr_1[,m], -sum(sigma_1[m] * beta_pr_1[,m]));
        
        // Compute level-2 coefficients
        vector[NJ] beta_2 = sigma_2[m] * beta_pr_2[,m];
        
        // Compute & store coefficients
        for (j in 1:NJ) {
            for (k in 1:NK) {
                beta[j,k,m] = beta_1[k] + beta_2[j];
            }
        }
    
    }

}
model {

    // Compute linear predictor
    vector[N] mu;
    for (n in 1:N)
        mu[n] = X1[n] * (beta_mu_01 + beta[J[n],K[n]]) + X2[n] * beta_mu_02;
        
    // Likelihood
    target += bernoulli_logit_lpmf(Y | mu);
    
    // Priors
    target += normal_lpdf(beta_mu_01 | 0, 2.5);
    target += normal_lpdf(beta_mu_02 | 0, 2.5);
    target += std_normal_lpdf(to_vector(beta_pr_1));
    target += std_normal_lpdf(to_vector(beta_pr_2));
    target += student_t_lpdf(sigma_1 | 3, 0, 1);
    target += student_t_lpdf(sigma_1 | 3, 0, 1);
    
}