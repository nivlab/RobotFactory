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

    // Group-level parameters
    matrix[5,2]           mu_pr;
    vector<lower=0>[5]    sigma_c;
    vector<lower=0>[5]    sigma_d;

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
    matrix<lower=-5, upper= 5>[N,2]  tau;
    matrix<lower=-1, upper= 1>[N,2]  nu;
    matrix<lower= 0, upper= 1>[N,2]  xi;

    // Session 1 parameters
    rho[:,1] = Phi_approx( mu_pr[1,1] + rho_c_pr*sigma_c[1] - rho_d_pr*sigma_d[1] ) * 20;
    eta[:,1] = Phi_approx( mu_pr[2,1] + eta_c_pr*sigma_c[2] - eta_d_pr*sigma_d[2] );
    tau[:,1] = tanh( mu_pr[3,1] + tau_c_pr*sigma_c[3] - tau_d_pr*sigma_d[3] ) * 5;
    nu[:,1]  = tanh( mu_pr[4,1] + nu_c_pr*sigma_c[4] -  nu_d_pr*sigma_d[4] );
    xi[:,1]  = Phi_approx( -1.645 + mu_pr[5,1] + xi_c_pr*sigma_c[5] - xi_d_pr*sigma_d[5] );

    // Session 2 parameters
    rho[:,2] = Phi_approx( mu_pr[1,2] + rho_c_pr*sigma_c[1] + rho_d_pr*sigma_d[1] ) * 20;
    eta[:,2] = Phi_approx( mu_pr[2,2] + eta_c_pr*sigma_c[2] + eta_d_pr*sigma_d[2] );
    tau[:,2] = tanh( mu_pr[3,2] + tau_c_pr*sigma_c[3] + tau_d_pr*sigma_d[3] ) * 5;
    nu[:,2]  = tanh( mu_pr[4,2] + nu_c_pr*sigma_c[4] +  nu_d_pr*sigma_d[4] );
    xi[:,2]  = Phi_approx( -1.645 + mu_pr[5,2] + xi_c_pr*sigma_c[5] + xi_d_pr*sigma_d[5] );

}
model {

    // Group-level priors
    to_vector(mu_pr) ~ normal(0,1);
    sigma_c ~ gamma(1,0.5);
    sigma_d ~ gamma(1,0.5);

    // Individual-level priors
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

    matrix[5,2] mu;
    vector[5] TRT;

    // Group-level means
    for (i in 1:2) {
      mu[1,i] = Phi_approx( mu_pr[1,i] ) * 20;
      mu[2,i] = Phi_approx( mu_pr[2,i] );
      mu[3,i] = tanh( mu_pr[3,i] ) * 5;
      mu[4,i] = tanh( mu_pr[4,i] );
      mu[5,i] = Phi_approx( -1.645 + mu_pr[5,i] );
    }

    // Test-retest reliability: Reward scale
    TRT[1] = (sigma_c[1] - sigma_d[1]) / (sigma_c[1] + sigma_d[1]);

    // Test-retest reliability: Learning rate
    TRT[2] = (sigma_c[2] - sigma_d[2]) / (sigma_c[2] + sigma_d[2]);

    // Test-retest reliability: Go bias
    TRT[3] = (sigma_c[3] - sigma_d[3]) / (sigma_c[3] + sigma_d[3]);

    // Test-retest reliability: Pavlovian bias
    TRT[4] = (sigma_c[4] - sigma_d[4]) / (sigma_c[4] + sigma_d[4]);

    // Test-retest reliability: Pavlovian bias
    TRT[5] = (sigma_c[5] - sigma_d[5]) / (sigma_c[5] + sigma_d[5]);

}
