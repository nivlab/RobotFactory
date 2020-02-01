data {

    // Metadata
    int  N;                         // Number of participants
    int  T;                         // Number of trials

    // Data
    int  Y[N,2,T];                  // Choices (Go = 1, No-Go = 0)
    int  X[N,2,T];                  // States
    real R[N,2,T];                  // Rewards (-1, 0, 1)

}
parameters {

    // Individual-level parameters
    vector[N]  rho_c_pr;            // Reward scale (common)
    vector[N]  rho_d_pr;            // Reward scale (deviation)

    vector[N]  eta_c_pr;            // Learning rate (common)
    vector[N]  eta_d_pr;            // Learning rate (deviation)

    vector[N]  tau_c_pr;            // Go bias (common)
    vector[N]  tau_d_pr;            // Go bias (deviation)

    vector[N]  nu_c_pr;             // Pavlovian bias (common)
    vector[N]  nu_d_pr;             // Pavlovian bias (deviation)

    vector[N]  xi_c_pr;             // Lapse rate (common)
    vector[N]  xi_d_pr;             // Lapse rate (deviation)

}
transformed parameters {

    matrix<lower= 0, upper=20>[N,2]  rho;
    matrix<lower= 0, upper= 1>[N,2]  eta;
    matrix<lower=-20, upper=20>[N,2]  tau;
    matrix<lower=-1, upper= 1>[N,2]  nu;
    matrix<lower= 0, upper= 1>[N,2]  xi;

    // Session 1 parameters
    rho[:,1] = Phi_approx( rho_c_pr - rho_d_pr ) * 20;
    eta[:,1] = Phi_approx( eta_c_pr - eta_d_pr );
    tau[:,1] = tanh( tau_c_pr - tau_d_pr ) .* rho[:,1];
    nu[:,1]  = tanh(  nu_c_pr -  nu_d_pr );
    xi[:,1]  = Phi_approx( -1.645 + xi_c_pr - xi_d_pr );

    // Session 2 parameters
    rho[:,2] = Phi_approx( rho_c_pr + rho_d_pr ) * 20;
    eta[:,2] = Phi_approx( eta_c_pr + eta_d_pr );
    tau[:,2] = tanh( tau_c_pr + tau_d_pr ) .* rho[:,2];
    nu[:,2]  = tanh(  nu_c_pr +  nu_d_pr );
    xi[:,2]  = Phi_approx( -1.645 + xi_c_pr + xi_d_pr );

}
model {

    // Individial-level priors
    rho_c_pr ~ normal(0, 1.0);
    rho_d_pr ~ normal(0, 0.5);

    eta_c_pr ~ normal(0, 1.0);
    eta_d_pr ~ normal(0, 0.5);

    tau_c_pr ~ normal(0, 1.0);
    tau_d_pr ~ normal(0, 0.5);

    nu_c_pr  ~ normal(0, 1.0);
    nu_d_pr  ~ normal(0, 0.5);

    xi_c_pr ~ normal(0, 1.0);
    xi_d_pr ~ normal(0, 0.5);


    // Iterate over participants
    for (i in 1:N) {

        // Iterate over sessions
        for (j in 1:2) {

            // Initialize quantities
            matrix[4,2] Q = rep_matrix(0, 4, 2);    // No-Go, Go
            vector[4]   V = rep_vector(0, 4);
            vector[T]   p = rep_vector(0, T);

            // Trial-by-trial learning
            for (k in 1:T) {

                // Compute likelihood of action
                p[k] = inv_logit( Q[X[i,j,k],2] - Q[X[i,j,k],1] + tau[i,j] + V[X[i,j,k]]*nu[i,j] );
                p[k] = (1- xi[i,j]) * p[k] + (xi[i,j] / 2);

                // Update action value.
                Q[X[i,j,k], Y[i,j,k]+1] += eta[i,j] * ( rho[i,j]*R[i,j,k] - Q[X[i,j,k], Y[i,j,k]+1] );

                // Update state value.
                V[X[i,j,k]] += eta[i,j] * ( rho[i,j] * R[i,j,k] - V[X[i,j,k]] );

            }

            // Likelihood
            Y[i,j] ~ bernoulli( p );

        }

    }

}
generated quantities {

    // Variances
    vector[5] sigma_c;
    vector[5] sigma_d;
    vector[5] TRT;

    // Test-retest reliability: Reward scale
    sigma_c[1] = variance(rho_c_pr);
    sigma_d[1] = variance(rho_d_pr);
    TRT[1] = (sigma_c[1] - sigma_d[1]) / (sigma_c[1] + sigma_d[1]);

    // Test-retest reliability: Learning rate
    sigma_c[2] = variance(eta_c_pr);
    sigma_d[2] = variance(eta_d_pr);
    TRT[2] = (sigma_c[2] - sigma_d[2]) / (sigma_c[2] + sigma_d[2]);

    // Test-retest reliability: Go bias
    sigma_c[3] = variance(tau_c_pr);
    sigma_d[3] = variance(tau_d_pr);
    TRT[3] = (sigma_c[3] - sigma_d[3]) / (sigma_c[3] + sigma_d[3]);

    // Test-retest reliability: Pavlovian bias
    sigma_c[4] = variance(nu_c_pr);
    sigma_d[4] = variance(nu_d_pr);
    TRT[4] = (sigma_c[4] - sigma_d[4]) / (sigma_c[4] + sigma_d[4]);

    // Test-retest reliability: Pavlovian bias
    sigma_c[5] = variance(xi_c_pr);
    sigma_d[5] = variance(xi_d_pr);
    TRT[5] = (sigma_c[5] - sigma_d[5]) / (sigma_c[5] + sigma_d[5]);

}
