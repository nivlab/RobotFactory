# attach packages
require(here)

# load data
pit_data <- read.csv(here("..", "data.csv"))

# recode responses to 1 (no response), 2 (left press), or 3 (right press)
pit_data$Choice <- pit_data$Choice + 1
pit_data$Target <- pit_data$Target + 1

# recode response as -1 if participant pressed the wrong go key (i.e. L when there was an R cue on the screen, and vice versa)
pit_data[pit_data$Target == 2 & pit_data$Choice == 3,"Choice"] <- -1
pit_data[pit_data$Target == 3 & pit_data$Choice == 2,"Choice"] <- -1
pit_data[pit_data$Choice > 1,"Choice"] <- 2

# rewrite colnames in a more familiar format
colnames(pit_data) <- c("id","cond","block","trial","exposure","state","valence","correct_action_type","target_action","response","correct","rt","outcome","diagnosis","state","trait")

# write resulting data out as clean_data.csv
write.csv(pit_data, file = here("dan_data.csv"), row.names=F)