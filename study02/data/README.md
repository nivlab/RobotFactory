# Data dictionaries

## Pavlovian go/no-go data

subject         object         subject id 
session         int64          session id {1, 2, 3}
block           int64          block order id {1, 2} 
runsheet       object          block groups, each session will use a different pair (pair is denotated by the digit) {'1a', '1b', '2a', '2b', '3a', '3b'}
trial           int64          trial id \[1, 240\]
exposure        int64          unique stim exposure (increasing) \[1- 12\]
valence        object          trial context, if lose- robots are GAL/NGAL. if win- robots are GW/NGW {'lose', 'win'}
action         object          correct action in words {'go', 'no-go'}
robot          object          robot type {'GAL', 'GW', 'NGAL', 'NGW'}
stimulus      float64          robot stim \[0-11\]
rune           object          the randomized face (symbol) for a stimulus \[A-Z\]
rune_set       object          font types for symbols {'bacs1', 'bacs2', 'elianto'}
correct         int64          correct action in  T/F {0,1}
choice          int64          subject's response  {0,1}
rt            float64          RT (s) 
accuracy        int64          the accuracy of the response (incorrect/correct) {0,1}
sham          float64          1 incorrect feedback / 0 correct feedback {0,1}
outcome         int64          reward {-10, -1, 1, 10}
total_keys      int64          # keyboard presses during the entire trial \[0-18\]
    

