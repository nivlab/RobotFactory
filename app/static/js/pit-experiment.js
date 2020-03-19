//------------------------------------//
// Define parameters.
//------------------------------------//

// Define timings.
const trial_duration = 1500;         // Duration of trial (response phase)
const feedback_duration = 1000;      // Duration of feedback (minimum)

// Define runes.
var runes = ['03','04','05','06'];
runes = jsPsych.randomization.sampleWithoutReplacement(runes, runes.length);

// Define scanner colors.
if (jsPsych.randomization.repeat([0,1],1)[0] == 1 ) {
  var instr_color_win    = 'blue';
  var scanner_color_win  = '#3366ff99';
  var outcome_color_win  = '#00539C';
  var instr_color_lose   = 'yellow';
  var scanner_color_lose = '#ffcc3399';
  var outcome_color_lose = '#ee9c00';
} else {
  var instr_color_win    = 'yellow';
  var scanner_color_win  = '#ffcc3399';
  var outcome_color_win  = '#ee9c00';
  var instr_color_lose   = 'blue';
  var scanner_color_lose = '#3366ff99';
  var outcome_color_lose = '#00539C';
}

//------------------------------------//
// Define instructions.
//------------------------------------//

var INSTRUCTIONS_01 = {
    type: 'pit-instructions',
    pages: [
      "Welcome to the<br><b>Robot Factory!</b>",
      "In this task, you will be inspecting robots as they move down the assembly line into the <b>scanner</b>.",
      "When a robot is scanned, you must decide whether to:<br><b>Approve</b> a robot as complete (press SPACE).<br><b>Reject</b> a robot as incomplete (do nothing).",
      "Next we will practice these actions.<br>Four robots will come down the assembly line.<br><b>Approve</b> each robot by pressing SPACE.",
      "<b>HINT:</b> Only press once the robot is in the scanner<br>and the scanner light comes on."
    ],
    show_clickable_nav: true,
    button_label_previous: "Prev",
    button_label_next: "Next"
}

var PRACTICE_GO = [];
for (var i=0; i<4; i++){
  var trial = {
    type: 'pit-trial',
    valence: 'Practice',
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

var INSTRUCTIONS_02 = {
    type: 'pit-instructions',
    pages: [
      "Great job!<br>Four more robots will come down the assembly line.<br><b>Reject</b> each robot by doing nothing.",
    ],
    show_clickable_nav: true,
    button_label_previous: "Prev",
    button_label_next: "Next"
}

var PRACTICE_NO_GO = [];
for (var i=0; i<4; i++){
  var trial = {
    type: 'pit-trial',
    valence: 'Practice',
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

var INSTRUCTIONS_03 = {
    type: 'pit-instructions',
    pages: [
      "During the task, the scanner will shine<br>one of two colors.",
      `If the scanner is <b><font color=${outcome_color_win}>${instr_color_win}</font></b>, you will earn +10 points for<br>correctly judging a robot as complete or incomplete.<br>Incorrect judgments will earn you +1 points.`,
      `If the scanner is <b><font color=${outcome_color_lose}>${instr_color_lose}</font></b>, you will earn -1 points for<br>correctly judging a robot as complete or incomplete.<br>Incorrect judgments will earn you -10 points.`,
      "When a robot is scanned, it will reveal a <b>symbol</b> on its<br>chestplate. This symbol will mark whether a robot is<br>complete or incomplete.",
      "Pay close attention to the symbol as it will help you<br>decide whether to accept (press SPACE)<br>or reject (do nothing) the robot.",
      "<b>Be aware:</b> Sometimes the scanner will malfunction and<br>provide you incorrect feedback. That is, it may provide<br>you the wrong number of points based on your judgment.",
      "At the end of the task, the total number of points you've<br>earned will be converted into a performance bonus.",
      "Next, we will ask you some questions about the task.",
    ],
    show_clickable_nav: true,
    button_label_previous: "Prev",
    button_label_next: "Next"
}

var COMPREHENSION = {
  type: 'pit-comprehension',
  win_color_text: instr_color_win,
  lose_color_text: instr_color_lose,
  win_color_hex: outcome_color_win,
  lose_color_hex: outcome_color_lose,
}

var INSTRUCTIONS_04 = {
    type: 'pit-instructions',
    pages: [
      "Get ready to begin the task.<br><br>Good luck!",
    ],
    show_clickable_nav: true,
    button_label_previous: "Prev",
    button_label_next: "Next"
}

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

  // Define single trial of experiment.
  var trial = {
    type: 'pit-trial',
    valence: trial.Valence,
    correct: trial.Correct,
    sham: trial.Sham,
    robot_rune: runes[trial.Robot-1],
    scanner_color: ((trial.Valence == 'Win') ? scanner_color_win : scanner_color_lose),
    outcome_color: ((trial.Valence == 'Win') ? outcome_color_win : outcome_color_lose),
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
    data: {
      Block: trial.Block,
      Trial: trial.Trial,
      Action: trial.Action,
      Robot: trial.Robot
    },
  };

  // Push to trial list.
  PIT_01.push(trial);

});

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


//------------------------------------//
// Define pause break.
//------------------------------------//


// Define pause trials.
var PAUSE = {
  type: 'pit-pause',
};

//------------------------------------//
// Define experiment (block 2).
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

  // Define single trial of experiment.
  var trial = {
    type: 'pit-trial',
    valence: trial.Valence,
    correct: trial.Correct,
    sham: trial.Sham,
    robot_rune: runes[trial.Robot-1],
    scanner_color: ((trial.Valence == 'Win') ? scanner_color_win : scanner_color_lose),
    outcome_color: ((trial.Valence == 'Win') ? outcome_color_win : outcome_color_lose),
    valid_responses: [32],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration,
    data: {
      Block: trial.Block,
      Trial: trial.Trial,
      Action: trial.Action,
      Robot: trial.Robot
    },
  };

  // Push to trial list.
  PIT_02.push(trial);

});
