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
      sham: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Sham trial',
        description: 'Denoting if trial is sham trial.'
      },
      valid_responses: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        array: true,
        pretty_name: 'Choices',
        default: [32],
        description: 'The keys the subject is allowed to press to respond to the stimulus.'
      },
      animation_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Animation duration',
        default: 1500,
        description: 'How long before keyboard listener should start.'
      },
      trial_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: 2000,
        description: 'How long to show trial before it ends.'
      },
      feedback_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Feedback duration',
        default: 500,
        description: 'How long to show feedback before it ends.'
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
    body {
      background: -webkit-gradient(linear, left bottom, left top, from(#808080), color-stop(50%, #606060), color-stop(50%, rgba(28, 25, 23, 0.5)), to(rgba(179, 230, 230, 0.5)));
      background: linear-gradient(0deg, #808080 0%, #606060 50%, #A0A0A0 50%, #D3D3D3 100%);
      height: 100vh;
      max-height: 100vh;
      overflow: hidden;
      position: fixed;
    }
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
    new_html += `<div class="machine-front"><div class="score-container"><div class="score" id="outcome"></div></div></div>`;
    new_html += '<div class="machine-top"></div>';
    new_html += '</div></div>';

    // Display HTML
    display_element.innerHTML = new_html;

    //---------------------------------------//
    // Response handling.
    //---------------------------------------//

    // Initialize response
    var response = {
      rt: -1,
      key: -1
    };

    // Feedback phase
    var after_response = function(info) {

      // Kill any timeout handlers / keyboard listeners
      jsPsych.pluginAPI.clearAllTimeouts();
      jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);

      // Record response (if any made)
      if (info != null) {
        response = info;
      }

      // Define accuracy
      if (trial.correct == -1 && response.key == -1) {
        response.accuracy = 1;
      } else if (trial.correct == 32 && response.key == 32) {
        response.accuracy = 1;
      } else {
        response.accuracy = 0;
      };

      // Define outcome
      if (trial.valence == "Win" && response.accuracy == 1 && trial.sham == 0) {
        trial.outcome = 1;
      } else if (trial.valence == "Win" && response.accuracy == 1 && trial.sham == 1) {
        trial.outcome = 0;
      } else if (trial.valence == "Win" && response.accuracy == 0 && trial.sham == 0) {
        trial.outcome = 0;
      } else if (trial.valence == "Win" && response.accuracy == 0 && trial.sham == 1) {
        trial.outcome = 1;
      } else if (trial.valence == "Lose" && response.accuracy == 1 && trial.sham == 0) {
        trial.outcome = 0;
      } else if (trial.valence == "Lose" && response.accuracy == 1 && trial.sham == 1) {
        trial.outcome = -1;
      } else if (trial.valence == "Lose" && response.accuracy == 0 && trial.sham == 0) {
        trial.outcome = -1;
      } else if (trial.valence == "Lose" && response.accuracy == 0 && trial.sham == 1) {
        trial.outcome = 0;
      }

      // Present outcome
      document.getElementById("outcome").innerHTML = trial.outcome;

      jsPsych.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.feedback_duration);

    };

    // End trial
    var end_trial = function() {

      // Kill any timeout handlers / keyboard listeners
      jsPsych.pluginAPI.clearAllTimeouts();
      if (typeof keyboardListener !== 'undefined') {
        jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
      }

      // Store data
      var trial_data = {
        "Correct": trial.correct,
        "Choice": response.key,
        "RT": response.rt,
        "Accuracy": response.accuracy,
        "Sham": trial.sham,
        "Outcome": trial.outcome,
      };

      // Clear the display
      display_element.innerHTML = '';

      // End trial
      jsPsych.finishTrial(trial_data);

    };

    // Start the response listener
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
      }, trial.animation_duration);

    }

    // End trial if trial_duration is set
    if (trial.trial_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        after_response();
      }, trial.animation_duration + trial.trial_duration);
    }

  };

  return plugin;
})();
