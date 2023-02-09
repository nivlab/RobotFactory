# Data dictionaries

## Pavlovian go/no-go data

- subject:    anonymized participant ID
- session:    session number (i.e., 1, 2, 3)
- block:      block number (i.e., 1, 2)
- runsheet:   trial structure (i.e., 1a, 1b, 2a, 2b, 3a, 3b)
- trial:      trial number
- exposure:   number of presentations (so far) of a given stimulus
- valence:    valence of trial (i.e., win, lose)
- action:     correct action for trial (i.e., go, no-go)
- robot:      trial type (i.e., go to win [gw], no-go to win [ngw], go to avoid losing [gal], no-go to avoid losing [ngal])
- stimulus:   bandit ID (i.e., 1-24)
- rune:       rune character
- rune_set:   character set (bacs1, bacs2, elianto)
- correct:    correct action (go = 1, no-go = 0)
- choice:     participant's choice (go = 1, no-go = 0)
- rt:         response time (s)
- accuracy:   scored choice (correct = 1, incorrect = 0)
- sham:       feedback type (correct = 0, incorrect = 1)
- outcome:    observed outcome
- total_keys: number of total button presses on that trial