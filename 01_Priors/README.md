Empirical Priors
================

Section Organization
--------------------

    ├── raw                  <- Compilation of previous collected PIT data.

Datasets
--------

| Handle | Repo | Subjects | Conditions | Trials | Valence | Feedback | Notes |
|--------|------|:--------:|:----------:|:------:|:-------:|:--------:|-------|
| [Albrecht et al. (2016)](https://doi.org/10.1371/journal.pone.0152781) | [Zenodo](https://zenodo.org/record/29601) | 32 | 4 | 192 | Unsignaled | 80% | Excluding SZ patients |
| [Mkrtchian et al. (2017)](https://doi.org/10.1016/j.biopsych.2017.01.017) | [Figshare](https://figshare.com/articles/Avoidance_Anxiety_Materials/3860250) | 101 | 4 | 480 | Unsignaled | 80% | HC = 58<br>Anx = 43<br>Safe/threat cond |
| [Millner et al. (2018)](https://doi.org/10.1162/jocn_a_01224) | [OSF](https://osf.io/p36u5/) | 52 | 4 | 240 | Signaled | 80% | Escape vs. avoidance |
| [Swart et al. (2018)](https://doi.org/10.1371/journal.pbio.2005979) | [Donders](https://data.donders.ru.nl/collections/di/dccn/DSC_3017033.03_624?0) | 34 | 8 | 320 | Unsignaled | 80% | |
| [Csifcsal et al. (2019)](https://doi.org/10.1162/jocn_a_01515) | [OSF](https://osf.io/89mdr/) | 23 | 4 | 720 | Unsignaled | 70% | Day 1 training available<br>Exclude yoked participants |
| [Csifcsal et al. (unpub)](https://doi.org/10.1162/jocn_a_01515) | [OSF](https://osf.io/d6eqk/) | 52 | 4 | 160 | Unsignaled | 70% | tDCS stimulation |

See notes on data cleaning.

Notes
-----

#### Mkrtchian et al. (2017)

- The task involves a target detection sub-task, wherein participants must identify and indicate the spatial location of a visual target. On a rare minority of trials, this results in erroneous responses on Go trials (e.g. participant correctly responds but incorrectly identifies the correct location of the target). Because on these trials the participant has successfuly learned the Go-rule, but has made a simple motor error (press wrong side button), we set these trials to NaNs. This should affect the overwhelming minority of participants in the sample.

#### Swart et al. (2018):

- 2 participants had a few (less than 5) missing outcomes. These were set to the most likely outcome given the trial condition and response.
- 43 trials had errors in keypress coding, i.e. not in [0, 97, 101]. The majority of these trials are too slow responses (>1300ms). These trials have their response values set to NaN. 