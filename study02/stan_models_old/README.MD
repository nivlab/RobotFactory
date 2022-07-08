
Models directory: 


Parameters dictionary: 
- $\epsilon$: learning rate
- $\rho$: feedback sensitivity
- $b$ : "go" bias
- $\pi$: static pavlovian bias 
- $\kappa$ : instrumental learning bias 


**OG paper :** Jennifer C SwartMonja I FroböseJennifer L CookDirk EM GeurtsMichael J FrankRoshan CoolsHanneke EM den Ouden (2017) Catecholaminergic challenge uncovers distinct Pavlovian and instrumental mechanisms of motivated (in)action eLife 6:e22169.

Their base model is:

M1 : $Q_t = Q_{t-1} + \epsilon (\rho r_t - Q_{t-1})$
M2: $$ Q_t =
     \begin{cases}
           \text{Q_t + \pi V(s)+b,} &\quad \text{if a=GO}\\
           \text{Q_t,} &\quad \text{else}\\

     \end{cases}$$

- mb_m1.stan - M1+B (Hanneke's M2, "go" bias model)
- mb_m2a.stan - M2+$\pi$ (Hanneke's M3a)
- mb_m2b.stan - M2+$\kappa$ (Hanneke's M3b)
- mb_m3.stan - M2+$\pi$+$\kappa$ (Hanneke's M4)


Naming convention 
-"mb" loosly refelcts "model based" models.
- "a" reflects learning rate (alpha)
- "b" reflects inverse temp (beta)

