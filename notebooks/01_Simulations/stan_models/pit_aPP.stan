data {

    // Metadata
    int  N;             // Number of participants
    int  K;             // Number of blocks
    int  S;             // Number of stimuli
    int  T;             // Number of trials
    
    // Data
    vector[N*S] R[K,T]; // Outcome data
    int  Y[K,T,N*S];    // Choice data (Go = 1, No-Go = 0)
    int  ix[N*S];       // Mapping of parameters to subjects
    
}
transformed data {
    
    // Vectorized choices
    vector[N*S]  y[K,T];
    
    for (i in 1:K) {
        for (j in 1:T) {
            y[i,j] = to_vector(Y[i,j]);
        }
    }
    
}
parameters {

    // Subject-level parameters
    vector[N]  beta_pr;
    vector[N]  eta_pr;
    vector[N]  tau_pr;
    vector[N]  nu_pr;

}
transformed parameters {

    vector<lower= 0, upper=10>[N]  beta;
    vector<lower= 0, upper= 1>[N]  eta;
    vector<lower=-1, upper= 1>[N]  tau;
    vector<lower=-1, upper= 1>[N]  nu;

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
        vector[N*S] Q1 = rep_vector(0, N*S);    // Go
        vector[N*S] Q2 = rep_vector(0, N*S);    // No-Go
        vector[N*S] V  = rep_vector(0, N*S);    // State value
        
        for (j in 1:T) {
        
            // Compute difference in expected value.
            vector[N*S] dEV = Q1 - Q2 + tau[ix] + nu[ix] .* V;
            
            // Likelihood.
            Y[i,j] ~ bernoulli_logit( beta[ix] .* dEV );
            
            // Update action value (go).
            Q1 += y[i,j] .* eta[ix] .* ( R[i,j] - Q1 );
            
            // Update action value (no-go).
            Q2 += (1-y[i,j]) .* eta[ix] .* ( R[i,j] - Q2 );
            
            // Update state value.
            V += eta[ix] .* ( R[i,j] - V );
            
        }
        
    }

}