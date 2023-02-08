version compatability

Stan 2.27+
cmdstanpy 1.0.4
CmdStan 2.27.0

see new syntax release notes https://blog.mc-stan.org/2021/06/04/release-of-cmdstan-2-27-0/



Models (See full documentation here: https://www.overleaf.com/2342646366xndvzcqrpdxm)
- m1.stan: RW Qlearning model:
    - eta (learning rate)
    - beta (inverse temp)
    
    
- m2.stan: RW Qlearning model + pavlovian bias: 
    - eta (learning rate)
    - beta (inverse temp)
    - beta_p (Pavlovian bias)
    
    
- m3.stan: RW Qlearning model + pavlovian bias + go bias: 
    - eta (learning rate)
    - beta (inverse temp)
    - beta_p (Pavlovian bias)
    - beta_GO (Go bias)
    
    
- m4.stan: RW Qlearning model + pavlovian bias + go bias + valance-based eta: 
    - \[eta_gain ,eta_loss\] (learning rate)
    - beta (inverse temp)
    - beta_p (Pavlovian bias)
    - versions
        - a: including beta_GO (Go bias) 
        - b: does not include go bias
    
    
- m5.stan: RW Qlearning model + pavlovian bias + go bias + contex(robot)-dependent asymmetry eta: 
    - \[eta_congurent ,eta_incongruent\] (learning rate, cong-GW, NGAL incong-NGW,GAL)
    - beta (inverse temp)
    - beta_p (Pavlovian bias)
    - versions
        - a: including beta_GO (Go bias) 
        - b: does not include go bias

    
- m6.stan: RW Qlearning model + pavlovian bias + go bias + outcome-dependent asymmetry eta: 
    - \[eta_congurent ,eta_incongruent\] (G(+) // NOGO(-))
    - beta (inverse temp)
    - beta_p (Pavlovian bias)
    - versions
        - a: including beta_GO (Go bias) 
        - b: does not include go bias
    
    
    
    

