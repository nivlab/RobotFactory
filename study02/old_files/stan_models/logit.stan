data {

    // Metadata
    int<lower=1>  N;                   // Number of total observations
    int<lower=1>  M;                   // Number of total endogenous effects
    int<lower=0>  K;                   // Number of total exogenous effects
    int<lower=1>  J[N];                // Subject-indicator per observation
    int<lower=1>  G[N];                // Session-indicator per observation
    
    // Data
    int  Y[N];                         // Response variable
    
    // Design matrix
    row_vector[M]  X[N];               // Endogenous variables
    row_vector[K]  Z[N];               // Exogenous variables

}
parameters {

    // Group-level effects
    matrix[M,2]  beta_mu;              // Group-level effects (endogenous)
    vector[K]    alpha;                // Group-level effects (exogenous)
    
    // Subject-level effects
    matrix[M,max(J)]  beta_c_pr;       // Between-subject effects
    matrix[M,max(J)]  beta_d_pr;       // Within-subject effects
    
    // Subject-level covariance
    cholesky_factor_corr[M] L_c;       // Cholesky factor of correlation matrix
    cholesky_factor_corr[M] L_d;       // Cholesky factor of correlation matrix
    matrix<lower=0>[M,2] sigma;        // Subject-level standard deviations

}
model {

    // Priors
    target += normal_lpdf(to_vector(beta_mu) | 0, 2.5);
    target += normal_lpdf(alpha | 0, 2.5);
    target += std_normal_lpdf(to_vector(beta_c_pr));
    target += std_normal_lpdf(to_vector(beta_d_pr));
    target += student_t_lpdf(to_vector(sigma) | 3, 0, 2.5);
    target += lkj_corr_cholesky_lpdf(L_c | 1);
    target += lkj_corr_cholesky_lpdf(L_d | 1);
    
    // Likelihood block
    {
     
    // Rotate random effects
    matrix[M,max(J)]  beta_c = diag_pre_multiply(sigma[:,1], L_c) * beta_c_pr;
    matrix[M,max(J)]  beta_d = diag_pre_multiply(sigma[:,2], L_d) * beta_d_pr;
                
    // Construct random effects
    vector[M] beta[2, max(J)];
    for (j in 1:max(J)) {
        beta[1,j] = beta_mu[,1] + beta_c[,j] - beta_d[,j];
        beta[2,j] = beta_mu[,2] + beta_c[,j] + beta_d[,j];
    }
    
    // Construct linear predictor terms
    vector[N] mu = rep_vector(0, N);
    for (n in 1:N) {
        mu[n] += X[n] * beta[G[n],J[n]] + Z[n] * alpha;
    }
    
    // Likelihood
    target += bernoulli_logit_lpmf(Y | mu);
    
    }

}
generated quantities {
    
    // Intra-class correlations
    vector[M]  rho = ( square(sigma[,1]) - square(sigma[,2]) )
                  ./ ( square(sigma[,1]) + square(sigma[,2]) );

}