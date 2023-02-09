data {

    // Metadata
    int<lower=1>  N;                        // Number of total observations
    int<lower=1>  K;                        // Number of total predictors
    
    // Data
    array[N] int<lower=0, upper=1>  Y;      // Response (go = 1, no-go = 0)
    
    // Design matrix
    matrix[N,K]  X;                         // Predictor variables

}
parameters {

    // Regression coefficients
    vector[K]  beta;                       // Population-level effects

}
model {

    // Likelihood
    target += bernoulli_logit_lpmf(Y | X * beta);
    
    // Priors
    target += normal_lpdf(beta | 0, 2.5);

}