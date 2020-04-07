// Pavlovian Instrumental Transfer (PIT) Task
// Model variant 1 (no pooling)
//
// Parameters (4): 
//   - beta: inverse temperature
//   - eta:  learning rate
//   - tau:  go bias
//   - nu:   Pavlovian bias
//
// Notes:
//   - Model is vectorized such that it iterates over all participants/arms
//   - Model requires no missing data 
//   - Requires mapping between participants (N) and data (H)
//   - Pavlovian bias constant across trials

data {

    // Metadata
    int  H;                         // Number of participants/blocks/arms
    int  T;                         // Number of trials
    
    // Mappings
    int        sub_ix[H];           // Trial-to-participant mapping
    vector[H]  pav_ix;              // Stimulus-to-valence mapping [Gain = 1, Loss = -1]
    
    // Data
    int       Y[2,T,H];             // Choices (Go = 1, No-Go = 0)
    vector[H] R[2,T];               // Rewards (-1, 0, 1)
    
}
transformed data {

    // Number of participants
    int  N = max(sub_ix);

    // Upper limit of inverse tmperature
    real  ul = 20;
    
    // Vectorized choices
    vector[H]  y[2,T];
    for (i in 1:2) {
        for (j in 1:T) {
            y[i,j] = to_vector(Y[i,j]);
        }
    }

}
parameters {
    
    // Inverse temperature
    vector[2]  beta_mu_pr;
    vector[N]  beta_c_pr;
    vector[N]  beta_d_pr;
    
    // Learning rate
    vector[2]  eta_mu_pr;
    vector[N]  eta_c_pr;
    vector[N]  eta_d_pr;

    // Go bias
    vector[2]  tau_mu_pr;
    vector[N]  tau_c_pr;
    vector[N]  tau_d_pr;
    
    // Pavlovian bias
    vector[2]  nu_mu_pr;
    vector[N]  nu_c_pr;
    vector[N]  nu_d_pr;
    
    // Variances
    vector<lower=0>[4] sigma_c;
    vector<lower=0>[4] sigma_d;

}
transformed parameters {

    vector<lower =  0, upper = ul>[N]  beta[2];
    vector<lower =  0, upper =  1>[N]  eta[2];
    vector<lower = -1, upper =  1>[N]  tau[2];
    vector<lower = -1, upper =  1>[N]  nu[2];
    
    // Session 1
    beta[1] = Phi_approx( beta_mu_pr[1] + sigma_c[1] * beta_c_pr - sigma_d[1] * beta_d_pr ) * ul;
    eta[1]  = Phi_approx( eta_mu_pr[1] + sigma_c[2] * eta_c_pr - sigma_d[2] * eta_d_pr );
    tau[1]  = tanh( tau_mu_pr[1] + sigma_c[3] * tau_c_pr - sigma_d[3] * tau_d_pr );
    nu[1]   = tanh( nu_mu_pr[1] + sigma_c[4] * nu_c_pr - sigma_d[4] * nu_d_pr );
    
    // Session 2
    beta[2] = Phi_approx( beta_mu_pr[2] + sigma_c[1] * beta_c_pr + sigma_d[1] * beta_d_pr ) * ul;
    eta[2]  = Phi_approx( eta_mu_pr[2] + sigma_c[2] * eta_c_pr + sigma_d[2] * eta_d_pr );
    tau[2]  = tanh( tau_mu_pr[2] + sigma_c[3] * tau_c_pr + sigma_d[3] * tau_d_pr );
    nu[2]   = tanh( nu_mu_pr[2] + sigma_c[4] * nu_c_pr + sigma_d[4] * nu_d_pr );
    
}
model {
        
    // Priors
    beta_mu_pr ~ normal(0, 1);
    beta_c_pr ~ normal(0, 1);
    beta_d_pr ~ normal(0, 1);
    
    eta_mu_pr ~ normal(0, 1);
    eta_c_pr ~ normal(0, 1);
    eta_d_pr ~ normal(0, 1);
    
    tau_mu_pr ~ normal(0, 1);
    tau_c_pr ~ normal(0, 1);
    tau_d_pr ~ normal(0, 1);
    
    nu_mu_pr ~ normal(0, 1);
    nu_c_pr ~ normal(0, 1);
    nu_d_pr ~ normal(0, 1);
    
    sigma_c ~ normal(0, 2);
    sigma_d ~ normal(0, 2);
    
    for (i in 1:2) {
    
        // Generated quantities
        matrix[H,T]  p  = rep_matrix(0, H, T);   // Go probability
        vector[H]    Q1 = pav_ix * 0.5;          // State-action values (go)
        vector[H]    Q2 = pav_ix * 0.5;          // State-action values (no-go)
        vector[H]    V  = pav_ix;                // State values

        // Parameter expansion
        vector[H]  beta_vec = beta[i][sub_ix];
        vector[H]  eta_vec = eta[i][sub_ix];
        vector[H]  tau_vec = tau[i][sub_ix];
        vector[H]  nu_vec  = nu[i][sub_ix];
    
        for (j in 1:T) {

            // Compute likelihood of acting (go)
            p[:,j] = beta_vec .* (Q1 - Q2 + tau_vec + nu_vec .* V );

            // Update action value (go)
            Q1 += y[i,j] .* ( eta_vec .* ( R[i,j] - Q1 ) );

            // Update action value (no-go)
            Q2 += (1-y[i,j]) .* ( eta_vec .* ( R[i,j] - Q2 ) );

        }

        // Likelihood
        to_array_1d(Y[i]) ~ bernoulli_logit( to_vector(p) );
        
    }
        
}
generated quantities {

    // Group-level parameters
    vector[2] beta_mu = Phi_approx(beta_mu_pr) * ul;
    vector[2] eta_mu = Phi_approx(eta_mu_pr);
    vector[2] tau_mu  = tanh(tau_mu_pr);
    vector[2] nu_mu  = tanh(nu_mu_pr);
    
    // Test-retest parameters
    vector[4] rho;
    for (i in 1:4) {
        rho[i] = (sigma_c[i]^2 - sigma_d[i]^2) / (sigma_c[i]^2 + sigma_d[i]^2);
    }


}