data {

    // Metadata
    int<lower=1>  N;                   // Number of total observations
    int<lower=1>  M;                   // Number of total fixed effects
    int<lower=1>  K;                   // Number of total random effects (subject-level)
    int<lower=1>  J[N];                // Subject-indicator per observation
    
    // Data
    int  Y[N];                         // Response variable
    
    // Design matrix
    matrix[N,M]  X;                    // Group-level design matrix
    row_vector[K]  Z[N];               // Subject-level predictors

}
transformed data {

    // Hard-coded metadata
    int  S = 3;                        // Number of sessions
    int  U = K/S;                      // Number of fixed effects

}
parameters {

    // Group-level effects
    vector[M]  beta_mu;                // Group-level effects
    
    // Subject-level effects
    matrix[K, max(J)]  beta_pr;        // Standardized subject-level effects
    
    // Subject-level covariance
    cholesky_factor_corr[S] L[U];      // Cholesky factor of correlation matrix
    vector<lower=0>[K] sigma;          // Subject-level standard deviations

}
model {

    // Priors
    target += normal_lpdf(beta_mu | 0, 2.5);
    target += std_normal_lpdf(to_vector(beta_pr));
    target += student_t_lpdf(sigma | 3, 0, 2.5) - 3 * student_t_lccdf(0 | 3, 0, 2.5);
    for (u in 1:U) { target += lkj_corr_cholesky_lpdf(L[u] | 1); }
    
    // Likelihood block
    {
    
    // Preallocate space
    matrix[K, K]      LBD = identity_matrix(K);
    matrix[K, max(J)] beta;
    
    // Construct lower block diagonal matrix
    for (u in 1:U) {
        int v = S*(u-1);
        LBD[v+2,v+1] = L[u,2,1];
        LBD[v+3,v+1] = L[u,3,1];
        LBD[v+3,v+2] = L[u,3,2];
    }
    
    // Scale subject-level effects
    beta = diag_pre_multiply(sigma, LBD) * beta_pr;
    
    // Initialize linear predictor term
    vector[N] mu = rep_vector(0, N);
    
    // Add random effects to linear predictor
    for (n in 1:N) { mu[n] += Z[n] * beta[,J[n]]; }
    
    // Likelihood
    target += bernoulli_logit_glm_lpmf(Y | X, mu, beta_mu);
    
    }

}
generated quantities {

    // Intra-class correlations 
    vector[K] rho = rep_vector(0, K);
    
    for (u in 1:U) {
    
        // Construct correlation matrix
        matrix[U,U] Omega = multiply_lower_tri_self_transpose(L[u]);
        
        // Extract ICCs
        int v = S*(u-1);
        rho[v+1] = Omega[2,1];
        rho[v+2] = Omega[3,1];
        rho[v+3] = Omega[3,2];
    
    }
    
}