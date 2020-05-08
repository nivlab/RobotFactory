//------------------------------------//
// Define parameters.
//------------------------------------//

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

// Define go key.
const key_go = 32;

// Define timings.
const trial_duration = 1500;         // Duration of trial (response phase)
const feedback_duration = 1000;      // Duration of feedback (minimum)

// Define comprehension threshold.
const max_errors = 1;

// Define quality threshold.
const threshold = 0.90;

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

var PRACTICE_GO = {
  timeline: [{
    type: 'pit-trial',
    robot_rune: '01',
    scanner_color: '#FFFFF080',
    outcome_color: '#000000',
    outcome_correct: '+10',
    outcome_incorrect: '+0',
    correct: key_go,
    valid_responses: [key_go],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration
  }],
  repetitions: 4,
  data: {
    Block: 0,
    Action: 'Go',
  }
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

var PRACTICE_NO_GO = {
  timeline: [{
    type: 'pit-trial',
    robot_rune: '02',
    scanner_color: '#FFFFF080',
    outcome_color: '#000000',
    outcome_correct: '+10',
    outcome_incorrect: '+0',
    correct: -1,
    valid_responses: [key_go],
    trial_duration: trial_duration,
    feedback_duration: feedback_duration
  }],
  repetitions: 4,
  data: {
    Block: 0,
    Action: 'No-Go',
  }
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
    robot_runes: [
      undefined,
      undefined,
      undefined,
      '01',
      '01',
      undefined,
      undefined,
      undefined,
    ],
    scanner_colors: [
      '#FFFFFF00',
      scanner_color_win,
      scanner_color_lose,
      '#FFFFF080',
      '#FFFFF080',
      '#FFFFFF00',
      '#FFFFFF00',
      '#FFFFFF00'
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

var INSTRUCTIONS = {
  timeline: [
    INSTRUCTIONS_01,
    PRACTICE_GO,
    INSTRUCTIONS_02,
    PRACTICE_NO_GO,
    INSTRUCTIONS_03,
    COMPREHENSION
  ],
  loop_function: function(data) {

    // Extract number of errors.
    const num_errors = data.values().slice(-1)[0].num_errors;

    // Check if instructions should repeat.
    if (num_errors > max_errors) {
      return true;
    } else {
      return false;
    }

  }
}

var READY = {
    type: 'pit-instructions',
    pages: [
      "Get ready to begin the task.<br><br>Good luck!",
    ],
    show_clickable_nav: true,
    button_label_previous: "Prev",
    button_label_next: "Next"
}

//------------------------------------//
// Define experiment.
//------------------------------------//
// One block of the PIT task is comprised of
// 30 exposures to four robots (GW, NGW, GAL, NGAL),
// i.e. 120 total trials. 80% of trials provide
// correct feedback, or 1/5 trials (in blocks)
// present sham feedback. There are 2 total blocks,
// or 60 total exposures per robot (240 total trials).

// Predefine sham trials (12 sets of 5 trials).
var sham = [[],[],[],[]];
for (var i=0; i<4; i++) {
  for (var j=0; j<12; j++) {
    sham[i] = sham[i].concat(jsPsych.randomization.repeat([0,0,0,0,1],1));
  }
}

// Iteratively define trials (60 per robot.)
var PIT = [];
var n = 0;
for (var i=0; i<60; i++) {

  // Define presentation order of 4 robots.
  const order = jsPsych.randomization.repeat([0,1,2,3],1);

  // Iteratively define and append PIT trials.
  order.forEach(function (robot) {

    // Predefine valence.
    const valence = Math.floor(robot / 2) == 0 ? 'Win' : 'Lose';

    // Predefine feedback.
    if (valence == 'Win' && sham[robot][i] == 0) {
      var outcome_correct   = '+10';
      var outcome_incorrect = '+1';
    } else if (valence == 'Win' && sham[robot][i] == 1) {
      var outcome_correct   = '+1';
      var outcome_incorrect = '+10';
    } else if (valence == 'Lose' && sham[robot][i] == 0) {
      var outcome_correct   = '-1';
      var outcome_incorrect = '-10';
    } else if (valence == 'Lose' && sham[robot][i] == 1) {
      var outcome_correct   = '-10';
      var outcome_incorrect = '-1';
    }

    const trial = {
      type: 'pit-trial',
      robot_rune: runes[robot],
      scanner_color: valence == 'Win' ? scanner_color_win : scanner_color_lose,
      outcome_color: valence == 'Win' ? outcome_color_win : outcome_color_lose,
      outcome_correct: outcome_correct,
      outcome_incorrect: outcome_incorrect,
      correct: robot % 2 == 0 ? key_go : -1,
      valid_responses: [key_go],
      trial_duration: trial_duration,
      feedback_duration: feedback_duration,
      data: {
        Block: Math.floor(n / 120) + 1,
        Trial: n + 1,
        Robot: robot + 1,
        Valence: valence,
        Action: robot % 2 == 0 ? 'Go' : 'No-Go',
        Sham: sham[robot][i],
        Color: valence == 'Win' ? instr_color_win : instr_color_lose,
      }
    };

    PIT.push(trial)
    n = n + 1;

  })

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
  if ( ((freqs[key_go] || 0) / denom) > threshold ) {
    var low_quality = true;
  } else if ( ((freqs[-1] || 0) / denom) > threshold ) {
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
