//------------------------------------//
// Instructions block #1.
//------------------------------------//

var instructions_01 = {
  type: 'pit-instructions',
  pages: [
    "Welcome to the <b>Robot Factory</b> game!",
    "In this game, you will be inspecting robots as they move down the assembly line into the <b>scanner</b>.",
    "The robots in the factory are sometimes in need of repair.",
    "When a robot is scanned, you must decide whether to:<br><b>Repair</b> the robot (press SPACE) <br><b>Ignore</b> the robot (do nothing)",
    "Next you will practice these actions.<br>Four robots will come down the assembly line.<br><b>Repair</b> each robot by pressing SPACE.",
    "<b>HINT:</b> Only press once the robot is in the scanner<br>and the scanner light comes on."
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_start: function(trial) {
    pass_message('starting instructions');
  }
}

var practice_go = {
  timeline: [{
    type: 'pit-trial',
    robot_rune: '',
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
    block: 0
  }
}

var instructions_02 = {
  type: 'pit-instructions',
  pages: [
    "Great job!<br>Four more robots will come down the assembly line.<br><b>Ignore</b> each robot by doing nothing.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next"
}

var practice_no_go = {
  timeline: [{
    type: 'pit-trial',
    robot_rune: '',
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
    block: 0
  }
}

var quiz_01 = {
  type: 'pit-comprehension',
  prompts: [
    "To <b>repair</b> a robot, what do you do?",
    "To <b>ignore</b> a robot, what do you do?",
  ],
  options: [
    ["Press SPACE", "Do nothing", "Press ENTER"],
    ["Press SPACE", "Do nothing", "Press ENTER"],
  ],
  correct: [
    "Press SPACE",
    "Do nothing",
  ]
}

//------------------------------------//
// Instructions block #2.
//------------------------------------//

var instructions_03 = {
  type: 'pit-instructions',
  pages: [
    "There are different types of robots in the factory.<br>Some types of robot will need repair <b>more often</b> than others.",
    "You can tell a robot's type by the <b>symbol</b> on its<br>chestplate as revealed by the scanner.",
    "<b>HINT:</b> Not all robots of the same type will need repair, but<br>some types of robots will need repair more often than others.",
    "During the game, you will earn the most points by fixing robots in need of repair and ignoring robots that do not.",
    `Importantly, how many points you can win or lose depends<br>on whether the robot is <b><font color=${outcome_color_win}>SAFE</font></b> or <b><font color=${outcome_color_lose}>DANGEROUS</font></b>.`,
    `When the scanner is <b><font color=${outcome_color_win}>${instr_color_win}</font></b>, the robot is <b><font color=${outcome_color_win}>SAFE</font></b>.<br>You will earn +10 points for correctly repairing or ignoring<br>a safe robot. Incorrect actions will earn you +1 point.`,
    `If the scanner is <b><font color=${outcome_color_lose}>${instr_color_lose}</font></b>, the robot is <b><font color=${outcome_color_lose}>DANGEROUS</font></b>.<br>You will lose only -1 point for correctly repairing or ignoring<br>a dangeorus robot. Incorrect actions will cost you -10 points.`,
    "Pay close attention to the robot's symbol as it will help you<br>decide whether to repair the robot (press SPACE)<br>or ignore the robot (do nothing).",
    "You should try to earn as many points as you can, even if it's not possibe to win points or avoid losing points on every round.",
    "At the end of the task, the total number of points you've<br>earned will be converted into a <b>performance bonus.</b>",
    "Next, we will ask you some questions about the task.<br>You need to answer all questions correctly to proceed.",
  ],
  robot_runes: [
    '', 'A', 'A', '', '', 'A', 'A', 'A', '', '', ''
  ],
  scanner_colors: [
    '#FFFFFF00', '#FFFFF080', '#FFFFF080', '#FFFFFF00', '#FFFFFF00',
    scanner_color_win, scanner_color_lose, '#FFFFF080', '#FFFFFF00', '#FFFFFF00', '#FFFFFF00'
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next"
}

var quiz_02 = {
  type: 'pit-comprehension',
  prompts: [
    `When the scanner light is <b><font color=${outcome_color_win}>${instr_color_win}</font></b>, how many points will you earn for a correct action?`,
    `When the scanner light is <b><font color=${outcome_color_lose}>${instr_color_lose}</font></b>, how many points will you earn for a correct action?`,
    "<i>True</i> or <i>False</i>: Some robots will need repair more often than others.",
    "<i>True</i> or <i>False</i>: The points I earn will affect my performance bonus."
  ],
  options: [
    ["+10", "+1", "-1", "-10"],
    ["+10", "+1", "-1", "-10"],
    ["True", "False"],
    ["True", "False"],
  ],
  correct: [
    "+10",
    "-1",
    "True",
    "True"
  ]
}

//------------------------------------//
// Construct instructions blocks.
//------------------------------------//

var INSTRUCTIONS_LOOP_01 = {
  timeline: [
    instructions_01,
    practice_go,
    instructions_02,
    practice_no_go,
    quiz_01
  ],
  loop_function: function(data) {

    // Extract number of errors.
    const num_errors = data.values().slice(-1)[0].num_errors;

    // Check if instructions should repeat.
    if (num_errors > 0) {
      return true;
    } else {
      return false;
    }

  }

}

var INSTRUCTIONS_LOOP_02 = {
  timeline: [
    instructions_03,
    quiz_02
  ],
  loop_function: function(data) {

    // Extract number of errors.
    const num_errors = data.values().slice(-1)[0].num_errors;

    // Check if instructions should repeat.
    if (num_errors > 0) {
      return true;
    } else {
      return false;
    }

  }

}
