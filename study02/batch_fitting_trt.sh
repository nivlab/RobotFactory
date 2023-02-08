#! /usr/bin/env bash

# run with sbatch batch_fitting.sh [modelname: m1, m2, m3] [1,2,3] [1,2,3]


#SBATCH --job-name 'mb_fit'                  ## name
#SBATCH --time=20:00:00                      ## time limit(HH:MM:SS)
#SBATCH --mem-per-cpu=1000                   ## memory (4G is default, in megabytes)
#SBATCH --cpus-per-task=4                    ## cpus (def 1)
#SBATCH --partition all                      ## partition



## logs/notifications
#SBATCH --mail-type ALL                      ## email notifications
#SBATCH --mail-user gili@princeton.edu       ## address 

#SBATCH --out '/jukebox/niv/gili/RobotFactory/logs/%A_%a.out'
#SBATCH --error '/jukebox/niv/gili/RobotFactory/logs/%A_%a.err'






cd /jukebox/niv/gili/RobotFactory/study02/


module load anacondapy/2021.11
module load cmdstan/2.27.0

source activate cmdstan

python stan_fit_scripts/fit_trt.py $1 $2 $3


