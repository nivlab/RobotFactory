data {

    // Metadata
    int  S;             // Number of stimuli
    int  T;             // Number of trials
    
    // Data
    vector[S] R[2,T];   // Outcome data
    int     Y[2,T,S];   // Choice data (Go = 1, No-Go = 0)
    
}
transformed data {
    
    // Vectorized choices
    vector[S]  y[2,T];
    
    for (i in 1:2) {
        for (j in 1:T) {
            y[i,j] = to_vector(Y[i,j]);
        }
    }
    
}
parameters {

    // Subject-level parameters
    real  beta_c_pr;
    real  beta_d_pr;
    
    real  eta_c_pr;
    real  eta_d_pr;
    
    real  tau_c_pr;
    real  tau_d_pr;
    
    real  nu_c_pr;
    real  nu_d_pr;

}
transformed parameters {

    vector<lower= 0, upper=10>[2]  beta;
    vector<lower= 0, upper= 1>[2]  eta;
    vector<lower=-1, upper= 1>[2]  tau;
    vector<lower=-1, upper= 1>[2]  nu;

    beta[1] = Phi_approx( beta_c_pr - beta_d_pr ) * 10;
    beta[2] = Phi_approx( beta_c_pr + beta_d_pr ) * 10;
    
    eta[1] = Phi_approx( eta_c_pr - eta_d_pr );
    eta[2] = Phi_approx( eta_c_pr + eta_d_pr );
    
    tau[1] = tanh( tau_c_pr - tau_d_pr );
    tau[2] = tanh( tau_c_pr + tau_d_pr );
    
    nu[1] = tanh( nu_c_pr - nu_d_pr );
    nu[2] = tanh( nu_c_pr + nu_d_pr );

}
model {

    // Priors
    beta_c_pr ~ normal(0,1.0);
    beta_d_pr ~ normal(0,0.5);
    
    eta_c_pr ~ normal(0,1.0);
    eta_d_pr ~ normal(0,0.5);
    
    tau_c_pr ~ normal(0,1.0);
    tau_d_pr ~ normal(0,0.5);
    
    nu_c_pr ~ normal(0,1.0);
    nu_d_pr ~ normal(0,0.5);
    
    // Likelihood
    for (i in 1:2) {
    
        // Initialize Q-values
        vector[S] Q1 = rep_vector(0, S);    // Go
        vector[S] Q2 = rep_vector(0, S);    // No-Go
        vector[S] V  = rep_vector(0, S);    // State value
        
        for (j in 1:T) {
        
            // Compute difference in expected value.
            vector[S] dEV = Q1 - Q2 + tau[i] + nu[i] * V;
            
            // Likelihood.
            Y[i,j] ~ bernoulli_logit( beta[i] * dEV );
            
            // Update action value (go).
            Q1 += eta[i] * y[i,j] .* ( R[i,j] - Q1 );
            
            // Update action value (no-go).
            Q2 += eta[i] * (1-y[i,j]) .* ( R[i,j] - Q2 );
            
            // Update state value.
            V += eta[i] * ( R[i,j] - V );
            
        }
        
    }

}