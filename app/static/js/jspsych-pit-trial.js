/**
 * jspsych-pit-trial
 **/

jsPsych.plugins["pit-trial"] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'pit-trial',
    description: '',
    parameters: {
      valence: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Valence',
        description: 'Valence of trial (win or loss).'
      },
      scanner_color: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Scanner color',
        description: 'Color of factory scanner light.'
      },
      robot_rune: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Robot rune',
        description: 'Rune to display on robot.'
      },
      correct: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        pretty_name: 'Correct response',
        description: 'Correct response for trial.'
      },
      valid_responses: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        array: true,
        pretty_name: 'Choices',
        default: [32, 37, 39],
        description: 'The keys the subject is allowed to press to respond to the stimulus.'
      },
      trial_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: null,
        description: 'How long to show trial before it ends.'
      },
      response_ends_trial: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Response ends trial',
        default: false,
        description: 'If true, trial will end when subject makes a response.'
      },

    }
  }

  plugin.trial = function(display_element, trial) {

    //---------------------------------------//
    // Define HTML.
    //---------------------------------------//

    // Initialize HTML.
    var new_html = '';

    // Insert CSS (window animation).
    new_html += `<style>
    @-webkit-keyframes pavlovian {
      0%    {background: rgba(0, 0, 0, 0);}
      90%   {background: rgba(0, 0, 0, 0);}
      100%  {background-color: ${trial.scanner_color};}
    }
    @keyframes pavlovian {
      0%    {background: rgba(0, 0, 0, 0);}
      90%   {background: rgba(0, 0, 0, 0);}
      100%  {background-color: ${trial.scanner_color};}
    }
     </style>`;

    // Add robot factor wrapper.
    new_html += '<div id="jspsych-pit-trial-stimulus"><div class="wrap">';

    // Add factory machine parts (back).
    new_html += '<div class="machine-back"></div>';
    new_html += '<div class="conveyor"></div>';
    new_html += '<div class="shadows"></div>';

    // Add robot 1 (active).
    new_html += '<div class="robot" style="left: 50vw; -webkit-animation: enter 1s; animation: enter 1s;">';
    new_html += '<div class="antenna"></div>';
    new_html += '<div class="head"></div>';
    new_html += '<div class="torso">';
    new_html += '<div class="left"></div>';
    new_html += '<div class="right"></div>';
    new_html += `<div class="rune"><img src="${trial.robot_rune}" style="height: 100%; width: 100%; object-fit: contain"></div></div>`;
    new_html += '<div class="foot"></div></div>';

    // Add robot 2 (hidden).
    new_html += '<div class="robot" style="left: 100vw; -webkit-animation: exit 1s; animation: exit 1s;">';
    new_html += '<div class="antenna"></div>';
    new_html += '<div class="head"></div>';
    new_html += '<div class="torso">';
    new_html += '<div class="left"></div>';
    new_html += '<div class="right"></div>';
    new_html += `<div class="rune"></div></div>`;
    new_html += '<div class="foot"></div></div>';

    // Add factory window.
    new_html += `<div class="window" style="background: ${trial.scanner_color}"></div>`;

    // Add factory machine parts (front).
    new_html += '<div class="machine-front"><div class="score-container"></div></div>';
    new_html += '<div class="machine-top"></div>';
    new_html += '</div></div>';

    // Display HTML
    display_element.innerHTML = new_html;

    //---------------------------------------//
    // Response handling.
    //---------------------------------------//

    // store response
    var response = {
      rt: null,
      key: null
    };

    // function to end trial when it is time
    var end_trial = function() {

      // kill any remaining setTimeout handlers
      jsPsych.pluginAPI.clearAllTimeouts();

      // kill keyboard listeners
      if (typeof keyboardListener !== 'undefined') {
        jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
      }

      // check accuracy
      if (trial.correct == -1 && response.key == null) {
        response.accuracy = 1;
      } else if (trial.correct == 32 && response.key == 32) {
        response.accuracy = 1;
      } else if (trial.correct == 37 && response.key == 37) {
        response.accuracy = 1;
      } else if (trial.correct == 39 && response.key == 39) {
        response.accuracy = 1;
      } else {
        response.accuracy = 0;
      };

      // define outcome
      if (trial.valence == "Win" && response.accuracy == 1) {
        trial.outcome = 1;
      } else if (trial.valence == "Lose" && response.accuracy == 0) {
        trial.outcome = -1;
      } else {
        trial.outcome = 0;
      }

      // define new score.
      const score_post = trial.score + trial.outcome;

      // gather the data to store for the trial
      var trial_data = {
        "Correct": trial.correct,
        "Choice": response.key,
        "RT": response.rt,
        "Accuracy": response.accuracy,
        "Outcome": trial.outcome,
        "Score": score_post
      };

      // clear the display
      display_element.innerHTML = '';

      // move on to the next trial
      jsPsych.finishTrial(trial_data);
    };

    // function to handle responses by the subject
    var after_response = function(info) {

      // after a valid response, the stimulus will have the CSS class 'responded'
      // which can be used to provide visual feedback that a response was recorded
      display_element.querySelector('#jspsych-pit-trial-stimulus').className += ' responded';

      // only record the first response
      if (response.key == null) {
        response = info;
      }

      if (trial.response_ends_trial) {
        end_trial();
      }
    };

    // start the response listener
    if (trial.valid_responses != jsPsych.NO_KEYS) {

      var keyboardListener = "";
      setTimeout(function() {
        keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
          callback_function: after_response,
          valid_responses: trial.valid_responses,
          rt_method: 'performance',
          persist: false,
          allow_held_key: false
        });
      }, 1500);

    }

    // end trial if trial_duration is set
    if (trial.trial_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.trial_duration);
    }

  };

  return plugin;
})();
