/**
 * jspsych-pit-pause
 **/

jsPsych.plugins["pit-pause"] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'pit-pause',
    description: '',
    parameters: {
      valid_responses: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        array: true,
        pretty_name: 'Choices',
        default: jsPsych.ALL_KEYS,
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
        default: true,
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

    // Insert CSS (turn off conveyor animation).
    new_html += `<style>.conveyor:after {-webkit-animation: none; animation: none;}</style>`;

    // Add robot factor wrapper.
    new_html += '<div id="jspsych-pit-pause-stimulus"><div class="wrap">';

    // Add factory machine parts (back).
    new_html += '<div class="machine-back"></div>';
    new_html += '<div class="conveyor"></div>';
    new_html += '<div class="shadows"></div>';

    // Add robot 1 (active).
    new_html += '<div class="robot" style="left: 50vw;">';
    new_html += '<div class="antenna"></div>';
    new_html += '<div class="head"></div>';
    new_html += '<div class="torso">';
    new_html += '<div class="left"></div>';
    new_html += '<div class="right"></div>';
    new_html += `<div class="rune"></div></div>`;
    new_html += '<div class="foot"></div></div>';

    // Do not add factory window.
    // new_html += `<div class="window" style="background: ${trial.scanner_color}"></div>`;

    // Add factory machine parts (front).
    new_html += '<div class="machine-front"><div class="score-container"></div></div>';
    new_html += '<div class="machine-top"></div>';
    new_html += '</div></div>';

    // Add pause screen.
    new_html += '<div class="pause-container"><div class="pause-message">';
    new_html += `<p>Great job! You've earned ${trial.score} points.</p><p>Take a break for a few moments and press any button when you are ready to continue.</p>`;
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

      // define new score.
      const score_post = trial.score + trial.outcome;

      // gather the data to store for the trial
      var trial_data = {
        "RT": response.rt,
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
      display_element.querySelector('#jspsych-pit-pause-stimulus').className += ' responded';

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
      }, 3000);

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
