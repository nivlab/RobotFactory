data {

    // Metadata
    int<lower=1>  N;                        // Number of total observations
    int<lower=1>  M1;                       // Number of within-participant predictors
    int<lower=1>  M2;                       // Number of between-participant predictors (rune sets)
    array[N] int<lower=1>  J;               // Participant-indicator per observation
    array[N] int<lower=1>  K;               // Session-indicator per observation
    
    // Data
    array[N] int<lower=0, upper=1>  Y;      // Outcome (choice or accuracy)
    
    // Design matrix
    array[N] row_vector[M1]  X1;            // Within-participant predictors
    array[N] row_vector[M2]  X2;            // Between-participant predictors (rune sets)

}
transformed data {

    int  NJ = max(J);                       // Total number of participants
    int  NK = max(K);                       // Total number of sessions

}
parameters {

    // Population-level effects
    vector[M1]   beta_mu_01;                // Within-participant effects (grand means)
    vector[M2-1] beta_mu_02_pr;             // Between-participant effects (rune sets)

    // Group-level variances
    vector<lower=0>[M1] sigma;              // Within-participant variability

    // Group-level effects
    array[M1] matrix[NJ,NK] beta_pr;        // Within-participant effects
    
}
transformed parameters {

    // Between-participant effects (sum-to-zero constraint)
    vector[M2] beta_mu_02 = append_row(beta_mu_02_pr, -sum(beta_mu_02_pr));

    // Within-participant effects
    array[NJ,NK] vector[M1] beta;
    
    for (m in 1:M1) {        
        for (j in 1:NJ) {
            for (k in 1:NK) {
                beta[j,k,m] = sigma[m] * beta_pr[m,j,k];
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
    target += normal_lpdf(beta_mu_02_pr | 0, 2.5);
    target += student_t_lpdf(sigma | 3, 0, 1);
    for (m in 1:M1)
        target += std_normal_lpdf(to_vector(beta_pr[m]));
    
}