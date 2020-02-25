//------------------------------------//
// Section 1: Define experiment
//------------------------------------//

// Define scanner colors.
const scanner_green = '#7ee87d99';
const scanner_red = '#e87db399';

// Define timings.
const trial_duration = 2000;
const feedback_duration = 500;

// Define runes.
var runes = ['../static/img/rune01.png', '../static/img/rune02.png', '../static/img/rune03.png',
             '../static/img/rune04.png', '../static/img/rune05.png', '../static/img/rune06.png'];
runes = jsPsych.randomization.sampleWithoutReplacement(runes, runes.length);

// Define trial metadata
var PARAMS = [
    {'Trial':  1, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial':  2, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial':  3, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial':  4, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial':  5, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial':  6, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial':  7, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial':  8, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial':  9, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 10, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 11, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 12, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 13, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 14, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 15, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 16, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 17, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 18, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 19, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 20, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 21, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 22, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 23, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 24, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 25, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 26, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 27, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 28, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 29, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 30, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 31, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 32, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 33, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 34, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 35, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 36, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 37, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 38, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 39, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 40, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 41, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 42, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 43, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 44, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 45, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 46, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 47, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 48, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 49, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 50, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 51, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 52, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 53, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 54, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 55, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 56, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 57, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 58, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 59, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 60, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 61, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 62, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 63, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 64, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 65, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 66, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 67, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 68, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 69, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 70, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 71, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 72, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 73, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1},
    {'Trial': 74, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 75, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 76, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 77, 'Valence': 'Win',  'Action': 'Go',    'Robot': 1, 'Correct': 32},
    {'Trial': 78, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 2, 'Correct': -1},
    {'Trial': 79, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 3, 'Correct': 32},
    {'Trial': 80, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 4, 'Correct': -1}
];

//------------------------------------//
// Section 2: Prepare experiment
//------------------------------------//

// Iteratively initialize trials.
var PIT = [];
PARAMS.forEach(function (trial) {

  // Define scanner color.
  if (trial.Valence == 'Win') {
    var scanner_color = scanner_green;
  } else {
    var scanner_color = scanner_red;
  };

  // Define single trial of experiment.
  var pit_trial = {

    timeline: [

      // Trial phase
      {
        type: 'pit-trial',
        valence: trial.Valence,
        scanner_color: scanner_color,
        robot_rune: runes[trial.Robot-1],
        correct: trial.Correct,
        valid_responses: [32],
        trial_duration: trial_duration + 1500,
        response_ends_trial: true,
        on_finish: function(trial) {
          score = jsPsych.data.getLastTrialData().values()[0].Score;
        }
      },

      // Feedback phase
      {
        type: 'pit-feedback',
        valence: trial.Valence,
        scanner_color: scanner_color,
        robot_rune: runes[trial.Robot-1],
        feedback_duration: feedback_duration,
        on_start: function(trial) {
          trial.feedback_duration = feedback_duration + (trial_duration - (jsPsych.data.getLastTrialData().values()[0].RT || trial_duration));
          trial.outcome = jsPsych.data.getLastTrialData().values()[0].Outcome;
        },
      }
    ],

    // Trial metadata.
    data: {
      Trial: trial.Trial,
      Valence: trial.Valence,
      Action: trial.Action
    }

  };

  // Push to trial list.
  PIT.push(pit_trial);

});

// Define pause trials.
var PAUSE = {
  type: 'pit-pause',
  on_start: function(trial) {
    trial.score = score;
  },
};

//------------------------------------//
// Section 2: Prepare practice trials
//------------------------------------//

var PRACTICE_GO = [
    {'Trial':  1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32},
    {'Trial':  2, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32},
    {'Trial':  3, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32},
    {'Trial':  4, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32},
];

var PRACTICE_01 = [];
PRACTICE_GO.forEach(function (trial) {

  // Define scanner color.
  if (trial.Valence == 'Win') {
    var scanner_color = scanner_green;
  } else {
    var scanner_color = scanner_red;
  };

  // Define single trial of experiment.
  var pit_trial = {

    timeline: [

      // Trial phase
      {
        type: 'pit-trial',
        valence: trial.Valence,
        scanner_color: scanner_color,
        robot_rune: '../static/img/rune07.png',
        correct: trial.Correct,
        valid_responses: [32],
        trial_duration: trial_duration + 1500,
        response_ends_trial: true,
      },

      // Feedback phase
      {
        type: 'pit-feedback',
        valence: trial.Valence,
        scanner_color: scanner_color,
        robot_rune: '../static/img/rune07.png',
        feedback_duration: feedback_duration,
        on_start: function(trial) {
          trial.feedback_duration = feedback_duration + (trial_duration - (jsPsych.data.getLastTrialData().values()[0].RT || trial_duration));
          trial.outcome = jsPsych.data.getLastTrialData().values()[0].Outcome;
        },
      }
    ],

    // Trial metadata.
    data: {
      Trial: trial.Trial,
      Valence: trial.Valence,
      Action: trial.Action
    }

  };

  // Push to trial list.
  PRACTICE_01.push(pit_trial);

});
