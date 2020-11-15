//------------------------------------//
// Define parameters.
//------------------------------------//

// Define comprehension threshold.
var max_errors = 0;
var max_loops = 2;
var num_loops = 0;

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
