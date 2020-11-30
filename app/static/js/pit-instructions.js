//------------------------------------//
// Define instructions text.
//------------------------------------//

var instructions_01 = {
  type: 'pit-instructions',
  pages: [
    "Welcome to the <b>Robot Factory</b> game!",
    "In this game, you will be inspecting robots as they move down the assembly line into the <b>scanner</b>.",
    "Sometimes a robot in the factory will need repair.<br>How often a robot will need repair <b>depends on its type.</b>",
    "There are many different types of robots. Each type of robot<br>can be identified by the <b>unique symbol</b> on its chestplate.",
    "When a robot enters the scanner, you must decide whether to:<br><b>Repair</b> the robot (press SPACE) <br><b>Ignore</b> the robot (do nothing)",
    "You will earn the most points by fixing robots that need repair and ignoring robots that do not.",
    `Importantly, how many points you can win or lose depends<br>on whether the robot is <b><font color=${outcome_color_win}>SAFE</font></b> or <b><font color=${outcome_color_lose}>DANGEROUS</font></b>.`,
    `If the scanner is <b><font color=${outcome_color_win}>${instr_color_win}</font></b>, the robot is <b><font color=${outcome_color_win}>SAFE</font></b>.<br>You will earn +10 points for correctly repairing or ignoring<br>a safe robot. You will earn only +1 point for incorrect actions.`,
    "Now let's practice with a safe robot. Try to learn if<br>you should repair (press SPACE) or ignore it (do nothing).<br><b>Remember:</b> you will earn +10 points for the correct action.",
    "<b>HINT:</b> Only press once the robot is in the scanner<br>and the scanner light comes on."
  ],
  robot_runes: [
    '', '', '', 'O', '', '', '', '', ''
  ],
  scanner_colors: [
    '#FFFFFF00', '#FFFFFF00', '#FFFFFF00', '#FFFFF080', '#FFFFFF00', '#FFFFFF00',
    '#FFFFFF00', scanner_color_win, scanner_color_win, scanner_color_win
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
  on_start: function(trial) {
    pass_message('starting instructions');
  }
}

var instructions_02 = {
  type: 'pit-instructions',
  pages: [
    "Good job! You learned this type of robot needed repair.",
    "Now let's practice for another type of safe robot.<br>Try to learn if you should repair this robot (press SPACE)<br>or ignore it (do nothing)."
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next"
}

var instructions_03 = {
  type: 'pit-instructions',
  pages: [
    `If the scanner is <b><font color=${outcome_color_lose}>${instr_color_lose}</font></b>, the robot is <b><font color=${outcome_color_lose}>DANGEROUS</font></b>.<br>You will lose only -1 point for correctly repairing or ignoring<br>a dangeorus robot. You will lose -10 points for incorrect actions.`,
    "Now let's practice for a dangerous robot. Try to learn if<br>you should repair it (press SPACE) or ignore it (do nothing).<br><b>Remember:</b> you will lose only -1 points for the correct action.",
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
}

var instructions_04 = {
  type: 'pit-instructions',
  pages: [
    "Good job! You learned this type of robot did NOT need repair.",
    "Now let's practice for another type of dangerous robot.<br>Try to learn if you should repair this robot (press SPACE)<br>or ignore it (do nothing)."
  ],
  show_clickable_nav: true,
  button_label_previous: "Prev",
  button_label_next: "Next",
}

var instructions_05 = {
  type: 'pit-instructions',
  pages: [
    "Great job! We're almost ready to begin the game.",
    "<b>Remember:</b> Not all robots of the same type will need repair, but<br>some types of robots will need repair more often than others.",
    "Pay close attention to the robot's symbol as it will help you<br>decide whether to repair the robot (press SPACE)<br>or ignore the robot (do nothing).",
    "Try to earn, and avoid losing, as many points as you can.",
    "At the end of the task, the total number of points you've<br>earned will be converted into a <b>performance bonus.</b>",
    "Next, we will ask you some questions about the task.<br>You need to answer all questions correctly to proceed.",
  ]
}

//------------------------------------//
// Define practice blocks.
//------------------------------------//

// Practice block (GW robot)
const practice_01_trial = {
  type: 'pit-trial',
  robot_rune: '1',
  scanner_color: scanner_color_win,
  outcome_color: outcome_color_win,
  outcome_correct: '+10',
  outcome_incorrect: '+1',
  correct: key_go,
  valid_responses: [key_go],
  trial_duration: trial_duration,
  feedback_duration: feedback_duration,
  data: {block: 0, practice: 1}
}

var practice_01 = {
  timeline: [practice_01_trial],
  loop_function: function(data) {

    // Extract accuracy from practice trials (type 1).
    const reducer = (accumulator, currentValue) => accumulator + currentValue;
    const practice = jsPsych.data.get().filter({practice: 1}).select('accuracy').values;
    const score = practice.slice(Math.max(practice.length - 3, 0)).reduce(reducer);

    // If less than 4 practice trials: loop.
    if ( practice.length < 4 ) {
      return true;

    // If last 3 not at all correct: loop.
    } else if ( score < 3 ) {
      return true;

    // Otherwise: end practice.
    } else {
      return false;
    }

  }
}

// Practice block (NGW robot)
const practice_02_trial = {
  type: 'pit-trial',
  robot_rune: '2',
  scanner_color: scanner_color_win,
  outcome_color: outcome_color_win,
  outcome_correct: '+10',
  outcome_incorrect: '+1',
  correct: -1,
  valid_responses: [key_go],
  trial_duration: trial_duration,
  feedback_duration: feedback_duration,
  data: {block: 0, practice: 2}
}

var practice_02 = {
  timeline: [practice_02_trial],
  loop_function: function(data) {

    // Extract accuracy from practice trials (type 2).
    const reducer = (accumulator, currentValue) => accumulator + currentValue;
    const practice = jsPsych.data.get().filter({practice: 2}).select('accuracy').values;
    const score = practice.slice(Math.max(practice.length - 3, 0)).reduce(reducer);

    // If less than 4 practice trials: loop.
    if ( practice.length < 4 ) {
      return true;

    // If last 3 not at all correct: loop.
    } else if ( score < 3 ) {
      return true;

    // Otherwise: end practice.
    } else {
      return false;
    }

  }
}

// Practice block (NGW robot)
const practice_03_trial = {
  type: 'pit-trial',
  robot_rune: '3',
  scanner_color: scanner_color_lose,
  outcome_color: outcome_color_lose,
  outcome_correct: '-1',
  outcome_incorrect: '-10',
  correct: -1,
  valid_responses: [key_go],
  trial_duration: trial_duration,
  feedback_duration: feedback_duration,
  data: {block: 0, practice: 3}
}

var practice_03 = {
  timeline: [practice_03_trial],
  loop_function: function(data) {

    // Extract accuracy from practice trials (type 3).
    const reducer = (accumulator, currentValue) => accumulator + currentValue;
    const practice = jsPsych.data.get().filter({practice: 3}).select('accuracy').values;
    const score = practice.slice(Math.max(practice.length - 3, 0)).reduce(reducer);

    // If less than 4 practice trials: loop.
    if ( practice.length < 4 ) {
      return true;

    // If last 3 not at all correct: loop.
    } else if ( score < 3 ) {
      return true;

    // Otherwise: end practice.
    } else {
      return false;
    }

  }
}

// Practice block (GAL robot)
const practice_04_trial = {
  type: 'pit-trial',
  robot_rune: '4',
  scanner_color: scanner_color_lose,
  outcome_color: outcome_color_lose,
  outcome_correct: '-1',
  outcome_incorrect: '-10',
  correct: key_go,
  valid_responses: [key_go],
  trial_duration: trial_duration,
  feedback_duration: feedback_duration,
  data: {block: 0, practice: 4}
}

// Practice block (GAL robot)
var practice_04 = {
  timeline: [practice_04_trial],
  loop_function: function(data) {

    // Extract accuracy from practice trials (type 4).
    const reducer = (accumulator, currentValue) => accumulator + currentValue;
    const practice = jsPsych.data.get().filter({practice: 4}).select('accuracy').values;
    const score = practice.slice(Math.max(practice.length - 3, 0)).reduce(reducer);

    // If less than 4 practice trials: loop.
    if ( practice.length < 4 ) {
      return true;

    // If last 3 not at all correct: loop.
    } else if ( score < 3 ) {
      return true;

    // Otherwise: end practice.
    } else {
      return false;
    }

  }
}

//------------------------------------//
// Define comprehension check.
//------------------------------------//

var quiz = {
  type: 'pit-comprehension',
  prompts: [
    "To <b>repair</b> a robot, what do you do?",
    `When the scanner light is <b><font color=${outcome_color_win}>${instr_color_win}</font></b>, how many points will you earn for a correct action?`,
    `When the scanner light is <b><font color=${outcome_color_lose}>${instr_color_lose}</font></b>, how many points will you earn for a correct action?`,
    "<i>True</i> or <i>False</i>: Some robots will need repair more often than others.",
    "<i>True</i> or <i>False</i>: The points I earn will affect my performance bonus."
  ],
  options: [
    ["Press SPACE", "Do nothing", "Press ENTER"],
    ["+10", "+1", "-1", "-10"],
    ["+10", "+1", "-1", "-10"],
    ["True", "False"],
    ["True", "False"],
  ],
  correct: [
    "Press SPACE",
    "+10",
    "-1",
    "True",
    "True"
  ]
}

//------------------------------------//
// Define instructions block.
//------------------------------------//

var INSTRUCTIONS = {
  timeline: [
    // instructions_01,
    // practice_01,
    // instructions_02,
    // practice_02,
    // instructions_03,
    // practice_03,
    // instructions_04,
    // practice_04,
    instructions_05,
    quiz
  ]
}
