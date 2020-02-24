data {

    // Metadata
    int  K;             // Number of blocks
    int  S;             // Number of stimuli
    int  T;             // Number of trials
    
    // Data
    vector[S] R[K,T];   // Outcome data
    int     Y[K,T,S];   // Choice data (Go = 1, No-Go = 0)
    
}
transformed data {
    
    // Vectorized choices
    vector[S]  y[K,T];
    
    for (i in 1:K) {
        for (j in 1:T) {
            y[i,j] = to_vector(Y[i,j]);
        }
    }
    
}
parameters {

    // Subject-level parameters
    real  beta_pr;
    real  eta_pr;
    real  tau_pr;
    real  nu_pr;

}
transformed parameters {

    real<lower= 0, upper=10>  beta;
    real<lower= 0, upper= 1>  eta;
    real<lower=-1, upper= 1>  tau;
    real<lower=-1, upper= 1>  nu;

    beta = Phi_approx( beta_pr ) * 10;
    eta  = Phi_approx( eta_pr );
    tau  = tanh( tau_pr );
    nu   = tanh( nu_pr );

}
model {

    // Priors
    beta_pr ~ std_normal();
    eta_pr  ~ std_normal();
    tau_pr  ~ std_normal();
    nu_pr   ~ std_normal();
    
    // Likelihood
    for (i in 1:K) {
    
        // Initialize Q-values
        vector[S] Q1 = rep_vector(0, S);    // Go
        vector[S] Q2 = rep_vector(0, S);    // No-Go
        vector[S] V  = rep_vector(0, S);    // State value
        
        for (j in 1:T) {
        
            // Compute difference in expected value.
            vector[S] dEV = Q1 - Q2 + tau + nu * V;
            
            // Likelihood.
            Y[i,j] ~ bernoulli_logit( beta * dEV );
            
            // Update action value (go).
            Q1 += eta * y[i,j] .* ( R[i,j] - Q1 );
            
            // Update action value (no-go).
            Q2 += eta * (1-y[i,j]) .* ( R[i,j] - Q2 );
            
            // Update state value.
            V += eta * ( R[i,j] - V );
            
        }
        
    }

}