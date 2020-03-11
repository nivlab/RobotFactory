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
var runes = ['03','04','05','06'];
runes = jsPsych.randomization.sampleWithoutReplacement(runes, runes.length);

//------------------------------------//
// Define experiment (block 1)
//------------------------------------//

// Define trial parameters
var BLOCK_01 = [
  {'Block': 1, 'Trial': 1, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 2, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 3, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 4, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 5, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 1, 'Trial': 6, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 7, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 8, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 9, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 10, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 11, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 12, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 13, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 14, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 15, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 16, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 1, 'Trial': 17, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 1, 'Trial': 18, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 19, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 1, 'Trial': 20, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 21, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 22, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 23, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 24, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 25, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 26, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 27, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 28, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 29, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 30, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 1, 'Trial': 31, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 1, 'Trial': 32, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 33, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 34, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 35, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 36, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 1, 'Trial': 37, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 1, 'Trial': 38, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 39, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 40, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 41, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 1, 'Trial': 42, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 43, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 44, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 45, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 46, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 1, 'Trial': 47, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 48, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 49, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 50, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 51, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 52, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 53, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 54, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 55, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 56, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 57, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 1, 'Trial': 58, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 59, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 1, 'Trial': 60, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 61, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 62, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 63, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 64, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 65, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 66, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 67, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 1, 'Trial': 68, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 69, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 1, 'Trial': 70, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 71, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 72, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 73, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 74, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 1, 'Trial': 75, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 76, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 77, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 1, 'Trial': 78, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 1, 'Trial': 79, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 1, 'Trial': 80, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0}
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
    sham: trial.Sham,
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
    data: {
      Block: trial.Block,
      Trial: trial.Trial,
      Valence: trial.Valence,
      Action: trial.Action,
      Robot: trial.Robot
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
  {'Block': 2, 'Trial': 81, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 82, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 83, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 84, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 85, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 86, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 87, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 88, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 89, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 2, 'Trial': 90, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 2, 'Trial': 91, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 92, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 93, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 94, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 95, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 96, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 2, 'Trial': 97, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 2, 'Trial': 98, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 99, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 100, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 101, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 102, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 103, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 2, 'Trial': 104, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 2, 'Trial': 105, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 106, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 107, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 108, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 109, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 110, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 111, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 112, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 113, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 114, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 115, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 2, 'Trial': 116, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 117, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 2, 'Trial': 118, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 119, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 120, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 121, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 122, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 123, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 124, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 2, 'Trial': 125, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 2, 'Trial': 126, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 127, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 128, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 129, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 130, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 131, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 132, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 133, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 134, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 135, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 136, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 137, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 2, 'Trial': 138, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 139, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 140, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 2, 'Trial': 141, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 2, 'Trial': 142, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 143, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 144, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 145, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 146, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 147, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 148, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 149, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 150, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 151, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 152, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 153, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 154, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 155, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 0},
  {'Block': 2, 'Trial': 156, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 157, 'Robot': 3, 'Valence': 'Lose', 'Action': 'Go', 'Correct': 32, 'Sham': 1},
  {'Block': 2, 'Trial': 158, 'Robot': 4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1, 'Sham': 1},
  {'Block': 2, 'Trial': 159, 'Robot': 2, 'Valence': 'Win', 'Action': 'No-Go', 'Correct': -1, 'Sham': 0},
  {'Block': 2, 'Trial': 160, 'Robot': 1, 'Valence': 'Win', 'Action': 'Go', 'Correct': 32, 'Sham': 1}
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
    sham: trial.Sham,
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
    data: {
      Block: trial.Block,
      Trial: trial.Trial,
      Valence: trial.Valence,
      Action: trial.Action,
      Robot: trial.Robot
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
};

//------------------------------------//
// Define practice trials
//------------------------------------//

var PRACTICE_GO = [];
for (var i=0; i<4; i++){
  var trial = {
    type: 'pit-trial',
    valence: 'Win',
    scanner_color: '#fffff080',
    robot_rune: '01',
    correct: 32,
    sham: 0,
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
    scanner_color: '#fffff080',
    robot_rune: '02',
    correct: -1,
    sham: 0,
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
  };
  PRACTICE_NO_GO.push(trial);
}

//------------------------------------//
// Define quality check
//------------------------------------//

var quality_check = function() {

  // Compute metadata.
  var choices = jsPsych.data.get().filter({Block: 1}).select('Choice');
  const freqs = choices.frequencies();
  const denom = choices.count();

  // Check if Go or No-Go responses comprise more than 90% of responses.
  if ( ((freqs[32] || 0) / denom) > 0.95 ) {
    var low_quality = true;
  } else if ( ((freqs[-1] || 0) / denom) > 0.95 ) {
    var low_quality = true;
  } else {
    var low_quality = false;
  }
  return low_quality;
}

var QUALITY_CHECK = {
  type: 'call-function',
  func: quality_check,
  on_finish: function(trial) {
    low_quality = jsPsych.data.getLastTrialData().values()[0].value;
    if (low_quality) { jsPsych.endExperiment(); }
  }
}
