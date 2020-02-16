data {

    // Metadata
    int  N;                         // Number of participants
    int  T;                         // Number of trials
    
    // Data
    int  Y[N,T];                    // Choices (Go = 1, No-Go = 0)
    int  X[N,T];                    // States
    real R[N,T];                    // Rewards (-1, 0, 1)
    
}
parameters {
    
    // Individual-level parameters
    vector[N]  rho_pr;              // Reward scale
    vector[N]  eta_pr;              // Learning rate
    vector[N]  tau_pr;              // Go bias
    vector[N]  nu_pr;               // Pavlovian bias
    vector<lower=0,upper=1>[N]  xi; // Lapse rate

}
transformed parameters {

    vector<lower= 0, upper=20>[N]  rho;
    vector<lower= 0, upper= 1>[N]  eta;
    vector<lower=-1, upper= 1>[N]  tau;
    vector<lower=-1, upper= 1>[N]  nu;
    
    rho = Phi_approx( rho_pr ) * 20;
    eta = Phi_approx( eta_pr );
    tau = tanh( tau_pr );
    nu  = tanh( nu_pr );
    
}
model {
    
    // Individial-level priors
    rho_pr ~ normal(0, 1);
    eta_pr ~ normal(0, 1);
    tau_pr ~ normal(0, 1);
    nu_pr  ~ normal(0, 1);
    xi ~ beta(1,10);
    
    for (i in 1:N) {
    
        // Initialize quantities 
        matrix[4,2] Q = rep_matrix(0, 4, 2);    // No-Go, Go
        vector[4]   V = rep_vector(0, 4);
        vector[T]   p = rep_vector(0, T);
        
        // Trial-by-trial learning
        for (j in 1:T) {
        
            // Compute likelihood of action
            p[j] = inv_logit( Q[X[i,j],2] - Q[X[i,j],1] + 20*tau[i] + V[X[i,j]]*nu[i] );
            p[j] = (1- xi[i]) * p[j] + (xi[i] / 2);
        
            // Update action value.
            Q[X[i,j], Y[i,j]+1] += eta[i] * ( rho[i] * R[i,j] - Q[X[i,j], Y[i,j]+1] );
            
            // Update state value.
            V[X[i,j]] += eta[i] * ( rho[i] * R[i,j] - V[X[i,j]] );
        
        }
        
        // Likelihood
        Y[i] ~ bernoulli( p );
    
    }
    

}