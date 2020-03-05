//------------------------------------//
// Define parameters
//------------------------------------//

// Define scanner colors.
const scanner_green = '#7ee87d99';
const scanner_red = '#e87db399';

// Define timings.
const trial_duration = 1500;         // Duration of trial (response phase)
const feedback_duration = 1000;      // Duration of feedback (minimum)

// Define runes.
var runes = ['../static/img/rune03.png', '../static/img/rune04.png', '../static/img/rune05.png',
             '../static/img/rune06.png', '../static/img/rune07.png', '../static/img/rune08.png',
             '../static/img/rune09.png', '../static/img/rune10.png'];
runes = jsPsych.randomization.sampleWithoutReplacement(runes, runes.length);

//------------------------------------//
// Define experiment (block 1)
//------------------------------------//

// Define trial parameters
var BLOCK_01 = [
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

// Iteratively define trials.
var PIT_01 = [];
BLOCK_01.forEach(function (trial) {

  // Define scanner color.
  if (trial.Valence == 'Win') {
    var scanner_color = scanner_green;
  } else {
    var scanner_color = scanner_red;
  };

  // Define single trial of experiment.
  var trial = {
    type: 'pit-trial',
    valence: trial.Valence,
    scanner_color: scanner_color,
    robot_rune: runes[trial.Robot-1],
    correct: trial.Correct,
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
    on_finish: function(trial) {
      score = score + parseInt(jsPsych.data.getLastTrialData().values()[0].Outcome);
    },
    data: {
      Trial: trial.Trial,
      Valence: trial.Valence,
      Action: trial.Action
    },
  };

  // Push to trial list.
  PIT_01.push(trial);

});

//------------------------------------//
// Define experiment (block 2)
//------------------------------------//

// Define trial parameters
var BLOCK_02 = [
  {'Trial':  81, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial':  82, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial':  83, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial':  84, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial':  85, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial':  86, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial':  87, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial':  88, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial':  89, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial':  90, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial':  91, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial':  92, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial':  93, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial':  94, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial':  95, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial':  96, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial':  97, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial':  98, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial':  99, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 100, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 101, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 102, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 103, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 104, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 105, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 106, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 107, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 108, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 109, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 110, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 111, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 112, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 113, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 114, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 115, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 116, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 117, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 118, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 119, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 120, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 121, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 122, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 123, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 124, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 125, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 126, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 127, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 128, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 129, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 130, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 131, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 132, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 133, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 134, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 135, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 136, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 137, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 138, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 139, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 140, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 141, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 142, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 143, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 144, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 145, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 146, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 147, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 148, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 149, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 150, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 151, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 152, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 153, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 154, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 155, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1},
  {'Trial': 156, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 157, 'Valence': 'Win',  'Action': 'No-Go', 'Robot': 6, 'Correct': -1},
  {'Trial': 158, 'Valence': 'Win',  'Action': 'Go',    'Robot': 5, 'Correct': 32},
  {'Trial': 159, 'Valence': 'Lose', 'Action': 'Go',    'Robot': 7, 'Correct': 32},
  {'Trial': 160, 'Valence': 'Lose', 'Action': 'No-Go', 'Robot': 8, 'Correct': -1}
];

// Iteratively define trials.
var PIT_02 = [];
BLOCK_02.forEach(function (trial) {

  // Define scanner color.
  if (trial.Valence == 'Win') {
    var scanner_color = scanner_green;
  } else {
    var scanner_color = scanner_red;
  };

  // Define single trial of experiment.
  var trial = {
    type: 'pit-trial',
    valence: trial.Valence,
    scanner_color: scanner_color,
    robot_rune: runes[trial.Robot-1],
    correct: trial.Correct,
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
    on_finish: function(trial) {
      score = score + jsPsych.data.getLastTrialData().values()[0].Outcome;
    },
    data: {
      Trial: trial.Trial,
      Valence: trial.Valence,
      Action: trial.Action
    },
  };

  // Push to trial list.
  PIT_02.push(trial);

});

//------------------------------------//
// Define pause trials
//------------------------------------//

// Define pause trials.
var PAUSE = {
  type: 'pit-pause',
  on_start: function(trial) {
    trial.score = score;
  },
};

//------------------------------------//
// Define practice trials
//------------------------------------//

var PRACTICE_GO = [];
for (var i=0; i<4; i++){
  var trial = {
    type: 'pit-trial',
    valence: 'Win',
    scanner_color: '#ffffcc80',
    robot_rune: '../static/img/rune01.png',
    correct: 32,
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
  };
  PRACTICE_GO.push(trial);
}

var PRACTICE_NO_GO = [];
for (var i=0; i<4; i++){
  var trial = {
    type: 'pit-trial',
    valence: 'Win',
    scanner_color: '#ffffcc80',
    robot_rune: '../static/img/rune02.png',
    correct: -1,
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
  };
  PRACTICE_NO_GO.push(trial);
}
