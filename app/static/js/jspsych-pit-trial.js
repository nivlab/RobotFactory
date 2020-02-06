/**
 * jspsych-pit-trial
 **/


jsPsych.plugins["pit-trial"] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'pit-trial',
    description: '',
    parameters: {
      choices: {
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

    // Define current score.
    var score = ("00" + trial.score).slice(-3);

    var new_html = `
    <!-- Display Score -->
    <div class="score-container">
      <div class="score">Score:</div>
      <div class="points" id="points">${score}</div>
    </div>

    <div id="jspsych-pit-trial-stimulus">

      <div class="wrap">

        <div class="machine-back"></div>
        <div class="conveyor"></div>
        <div class="shadows"></div>

        <!-- Robot 1 -->
        <div class="robot" style="left: -10vw">
          <div class="antenna"></div>
          <div class="head"></div>
          <div class="torso">
            <div class="left"></div>
            <div class="right"></div>
          </div>
          <div class="foot"></div>
        </div>

        <!-- Robot 2 -->
        <div class="robot" style="left: 20vw">
          <div class="antenna"></div>
          <div class="head"></div>
          <div class="torso">
            <div class="left"></div>
            <div class="right"></div>
          </div>
          <div class="foot"></div>
        </div>

        <!-- Robot 3 -->
        <div class="robot" style="left: 50vw">
          <div class="antenna"></div>
          <div class="head"></div>
          <div class="torso">
            <div class="left"></div>
            <div class="right"></div>
          </div>
          <div class="foot"></div>
        </div>

        <!-- Robot 4 -->
        <div class="robot" style="left: 80vw">
          <div class="antenna"></div>
          <div class="head"></div>
          <div class="torso">
            <div class="left"></div>
            <div class="right"></div>
          </div>
          <div class="foot"></div>
        </div>

        <!-- Robot 5 -->
        <div class="robot" style="left: 110vw">
          <div class="antenna"></div>
          <div class="head"></div>
          <div class="torso">
            <div class="left"></div>
            <div class="right"></div>
          </div>
          <div class="foot"></div>
        </div>

        <div class="window"></div>
        <div class="machine-front"></div>
        <div class="machine-top"></div>

      </div>

    </div>`;

    // draw
    display_element.innerHTML = new_html;

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

      // gather the data to store for the trial
      var trial_data = {
        "rt": response.rt,
        "stimulus": trial.stimulus,
        "key_press": response.key,
        "score": trial.score + 1
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
    if (trial.choices != jsPsych.NO_KEYS) {

      var keyboardListener = "";
      setTimeout(function() {
        keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
          callback_function: after_response,
          valid_responses: trial.choices,
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
