functions {

    real rlddm_lpdf(int[] Y, vector Z, vector X, vector beta, vector alpha, vector tau, vector delta ) {
    
        // Define metadata
        int n = sum( to_row_vector(Y) .* X );
        int m = sum( (1 - to_row_vector(Y)) .* X );
        
        // Preallocate space
        int go_ix[n];
        int nogo_ix[m];
        int c1 = 1;
        int c2 = 1;
        
        // Define indices
        for (i in 1:len(Y)) {
        
            if ( X[i] == 1 && Y[i] == 1 ) {
                go_ix[c1] = i;
                c1 += 1;
            } else if ( X[i] == 1 && Y[i] == 0 ) {
                nogo_ix[c2] = i;
                c2 += 1;
            }
            
        }
        
        return ( wiener_lpdf( Y[go_ix] | alpha[go_ix], tau[go_ix], beta[go_ix], delta[go_ix] ) +
                 bernoulli_logit_lpmf( Y[nogo_ix] | beta[nogo_ix] ) )
    
    }

}
data {

    // Metadata
    int  H;                  // Number of subjects x robots 
    int  T;                  // Number of exposures
    
    // Data
    int        Y[T,H];       // Action (Go = 1, No-Go = 0)
    vector[H]  Z[T,H];       // Response times
    vector[H]  R[T];         // Rewards
    
    // Mappings
    int        sub_ix[H];    // Robot-to-subject mapping
    vector[H]  obs_ix[T];    // Trial      
    
}
parameters {



}
transformed parameters {



}
model {

// Priors
    to_vector(theta_pr) ~ std_normal();
    
    // Likelihood block
    {
    
    // Parameter expansion
    vector[H]  beta_vec = beta[sub_ix];
    vector[H]  eta_vec = eta[sub_ix];
    
    // Generated quantities
    vector[H]  Q1 = rep_vector(0.5, H);
    vector[H]  Q2 = rep_vector(0.5, H);
    
    // Likelihood (all robots)
    for (i in 1:T) {
    
        // Compute action likelihood
        Y[i] ~ bernoulli_logit( obs_ix[i] .* beta_vec .* (Q1 - Q2) );
        
        // Update action value (go)
        Q1 += one_hot[i] .* ( eta_vec .* ( R[i] - Q1 ) );
        
        // Update action value (no-go)
        Q2 += (1-one_hot[i]) .* ( eta_vec .* ( R[i] - Q2 ) );
    
    }
    
    }

}