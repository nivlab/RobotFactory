//------------------------------------//
// Define parameters.
//------------------------------------//

// Define runsheets
runsheets = jsPsych.randomization.shuffle(runsheets)

// Define aesthetics.
if ( Math.random() < 0.5 ) {
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

// Define runes.
const alphabet = 'BCDEFGHIJKLMNPQRSTUVWXYZ'.split('');
const runes = jsPsych.randomization.sampleWithoutReplacement(alphabet, 24);

// Define go key.
const key_go = 32;

// Define timings.
const trial_duration = 1300;         // Duration of trial (response phase)
const feedback_duration = 1200;      // Duration of feedback (minimum)

// Define payment.
const completion_bonus = 0.00;
const performance_bonus = 1.50;

//------------------------------------//
// Define experiment.
//------------------------------------//
// One block of the PIT task is comprised of 8-12 exposures to 12 robots, or
// 120 total trials. 80% of trials provide correct feedback. There are 2 total
// blocks, or 240 total trials.

// Preallocate space.
var PIT = [];

// Iteratively define trials.
var n = 0;
for (let i=0; i<runsheets.length; i++) {

  for (let j=0; j<runsheets[i]['robots'].length; j++) {

    jsPsych.randomization.shuffle([0,1,2,3]).forEach(function (k) {

      // Extract trial information.
      const robot    = runsheets[i]['robots'][j][k];
      const stimulus = runsheets[i]['stimuli'][j][k];

      // Define trial metadata.
      const valence = (robot < 2) ? 'win' : 'lose';
      const action = (robot % 2 == 0) ? 'go' : 'no-go';

      // Define trial outcomes.
      const sham = (Math.random() < 0.8) ? 0 : 1;
      if (valence == 'win' && sham == 0) {
        var outcome_correct   = '+10';
        var outcome_incorrect = '+1';
      } else if (valence == 'win') {
        var outcome_correct   = '+1';
        var outcome_incorrect = '+10';
      } else if (valence == 'lose' && sham == 0) {
        var outcome_correct   = '-1';
        var outcome_incorrect = '-10';
      } else {
        var outcome_correct   = '-10';
        var outcome_incorrect = '-1';
      }

      // Define trial.
      const trial = {
        type: 'pit-trial',
        robot_rune: runes[i*12 + stimulus],
        scanner_color: valence == 'win' ? scanner_color_win : scanner_color_lose,
        outcome_color: valence == 'win' ? outcome_color_win : outcome_color_lose,
        outcome_correct: outcome_correct,
        outcome_incorrect: outcome_incorrect,
        correct: robot % 2 == 0 ? key_go : -1,
        valid_responses: [key_go],
        trial_duration: trial_duration,
        feedback_duration: feedback_duration,
        data: {
          block: i + 1,
          trial: n + 1,
          robot: robot + 1,
          valence: valence,
          action: action,
          sham: sham
        }
      };

      // Append.
      PIT.push(trial)
      n++;

    })

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
    "Get ready to begin <b>Block 1/2</b>. It will take ~7 minutes.<br>Press next when you're ready to start.",
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
    "Get ready to begin <b>Block 2/2</b>. It will take ~7 minutes.<br>Press next when you're ready to start.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_finish: function(trial) {
    pass_message('starting block 2');
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
