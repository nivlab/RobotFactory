//------------------------------------//
// Define parameters.
//------------------------------------//

// Rune sets (uncomment to choose which to use).
const rune_s1 = ['rune_01_ear', 'rune_01_ger', 'rune_01_ingwaz', 'rune_01_yr'];
const rune_s2 = ['rune_02_cen', 'rune_02_haglaz', 'rune_02_os', 'rune_02_raido']
// const rune_s1 = ['rune_03_algiz', 'rune_03_naudiz', 'rune_03_othalan', 'rune_03_uruz'];
// const rune_s2 = ['rune_04_ac', 'rune_04_dalgaz', 'rune_04_iwaz', 'rune_04_wunjo'];
// const rune_s1 = ['rune_05_gebo', 'rune_05_ior', 'rune_05_jeran', 'rune_05_tiwaz'];
// const rune_s2 = ['rune_06_ansuz', 'rune_06_berkanan', 'rune_06_cweord', 'rune_06_ehwaz'];
// const rune_s1 = ['rune_07_gar', 'rune_07_kauna', 'rune_07_laukaz', 'rune_07_thurisaz'];
// const rune_s2 = ['rune_08_fehu', 'rune_08_mannaz', 'rune_08_pertho', 'rune_08_sigel'];

// Define runes.
var runes = jsPsych.randomization.shuffle([
  jsPsych.randomization.shuffle(rune_s1),
  jsPsych.randomization.shuffle(rune_s2)
]);

// Define scanner colors.
if ( jsPsych.randomization.repeat([0,1],1)[0] == 1 ) {
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
var max_errors = 0;
var max_loops = 2;
var num_loops = 0;

// Define accuracy threshold.
const threshold = 0.90;

// Define payment.
const completion_bonus = 0.00;
const performance_bonus = 1.50;

//------------------------------------//
// Define images for preloading.
//------------------------------------//

var rune_stimuli = ['../static/img/rune_00_ingz.png', '../static/img/rune_00_isaz.png'];
[].concat.apply([],runes).forEach(function(rune) {
  rune_stimuli.push('../static/img/' + rune + '.png')
})

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
    button_label_next: "Next",
    on_start: function(trial) {
      pass_message('starting instructions');
    }
}

var PRACTICE_GO = {
  timeline: [{
    type: 'pit-trial',
    robot_rune: 'rune_00_ingz',
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
    robot_rune: 'rune_00_isaz',
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
      "At the end of the task, the total number of points you've<br>earned will be converted into a <b>performance bonus.</b>",
      "Next, we will ask you some questions about the task.<br>You need to answer all questions correctly to proceed.",
    ],
    robot_runes: [
      undefined,
      undefined,
      undefined,
      'rune_00_ingz',
      'rune_00_ingz',
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
      num_loops++;
      if (num_loops >= max_loops) {
        low_quality = true;
        return false;
      } else {
        return true;
      }
    } else {
      return false;
    }

  }
}

var COMPREHENSION_CHECK = {
  type: 'call-function',
  func: function(){},
  on_finish: function(trial) {
    if (low_quality) { jsPsych.endExperiment(); }
  }
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

// Predefine sham trials (6 sets of 5 trials for each of 8 robots).
var sham = [[],[],[],[],[],[],[],[]];
for (var i=0; i<8; i++) {
  for (var j=0; j<6; j++) {
    sham[i] = sham[i].concat(jsPsych.randomization.repeat([0,0,0,0,1],1));
  }
}

// Iteratively define trials (2 blocks, 30 exposures per robot).
var PIT = [];
var n = 0;
for (var b=0; b<2; b++) {

  for (var i=0; i<30; i++) {

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
        robot_rune: runes[b][robot],
        scanner_color: valence == 'Win' ? scanner_color_win : scanner_color_lose,
        outcome_color: valence == 'Win' ? outcome_color_win : outcome_color_lose,
        outcome_correct: outcome_correct,
        outcome_incorrect: outcome_incorrect,
        correct: robot % 2 == 0 ? key_go : -1,
        valid_responses: [key_go],
        trial_duration: trial_duration,
        feedback_duration: feedback_duration,
        data: {
          Block: b + 1,
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

}

//------------------------------------//
// Define quality check
//------------------------------------//
// Check PIT accuracy after first block. Reject participants
// who respond consistently (go or no-go) on 90% or more trials.

var accuracy_check = function() {

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

var ACCURACY_CHECK = {
  type: 'call-function',
  func: accuracy_check,
  on_finish: function(trial) {
    low_quality = jsPsych.data.getLastTrialData().values()[0].value;
    if (low_quality) { jsPsych.endExperiment(); }
  }
}

//------------------------------------//
// Define transition screens.
//------------------------------------//

// Define ready screen.
var READY_01 = {
  type: 'pit-instructions',
  pages: [
    "Great job! You've passed the comprehension check.",
    "Get ready to begin <b>Block 1/4</b>. It will take ~3 minutes.<br>Press next when you're ready to start.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(trial) {
    pass_message('starting block 1');
  }
}

var READY_02 = {
  type: 'pit-instructions',
  pages: [
    "Take a break for a few moments and press any button when you are ready to continue.",
    "Get ready to begin <b>Block 2/4</b>. It will take ~3 minutes.<br>Press next when you're ready to start.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(trial) {
    pass_message('starting block 2');
  }
}

var READY_03 = {
  type: 'pit-instructions',
  pages: [
    "Take a break for a few moments and press any button when you are ready to continue.",
    "In the final two blocks, you will judge <b>brand new robots</b>.",
    "Get ready to begin <b>Block 3/4</b>. It will take ~3 minutes.<br>Press next you're ready to start.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(trial) {
    pass_message('starting block 3');
  }
}

var READY_04 = {
  type: 'pit-instructions',
  pages: [
    "Take a break for a few moments and press any button when you are ready to continue.",
    "Get ready to begin <b>Block 4/4</b>. It will take ~3 minutes.<br>Press next when you're ready to start.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(trial) {
    pass_message('starting block 4');
  }
}

// Define finish screen.
var FINISHED = {
  type: 'pit-instructions',
  pages: [
    "Great job! You've finished the task.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
}

// Define feedback screen.
var FEEDBACK = {
  stimulus: '',
  type: 'html-keyboard-response',
  on_start: function(trial) {

    // Compute overall accuracy.
    var accuracy = jsPsych.data.get().filter([{Block: 1}, {Block:2}]).select('Accuracy');
    var accuracy = accuracy.mean();

    // Compute payment.
    var bonus = completion_bonus + Math.ceil(performance_bonus * accuracy * 100) / 100;
    var total = completion_bonus + performance_bonus;

    // Report accuracy to subject.
    trial.stimulus = `You earned a bonus of $${bonus} out of $${total}.<br><br>Press any key to complete the experiment.`

  },
  on_finish: function(trial) {

    // Compute overall accuracy.
    var accuracy = jsPsych.data.get().filter([{Block: 1}, {Block:2}]).select('Accuracy');
    var accuracy = accuracy.mean();
    trial.accuracy = accuracy;

    // Compute payment.
    var bonus = completion_bonus + Math.ceil(performance_bonus * accuracy * 100) / 100;
    var total = completion_bonus + performance_bonus;
    trial.bonus = bonus;

  }
}
