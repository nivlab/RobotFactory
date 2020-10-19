/**
* jspsych-pit-trial
* Sam Zorowitz
*
* plugin for running a trial of modified risk sensitivity task
*
**/

jsPsych.plugins["pit-trial"] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'pit-trial',
    description: '',
    parameters: {
      valence: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Valence',
        description: ''
      },
      image: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Card suit left',
        description: ''
      },
      valid_responses: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        array: true,
        pretty_name: 'Valid responses',
        default: [32],
        description: 'The keys the subject is allowed to press to respond to the stimulus.'
      },
      choice_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: 1000,
        description: 'How long to show trial before it ends.'
      },
      feedback_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Feedback duration',
        default: 1500,
        description: 'How long to show feedback before it ends.'
      },
      animation_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Feedback duration',
        default: 900,
        description: 'How long to show feedback before it ends.'
      }
    }
  }

  plugin.trial = function(display_element, trial) {

    //---------------------------------------//
    // Define HTML.
    //---------------------------------------//

    // Initialize HTML.
    var new_html = '';

    // Insert CSS.
    new_html += `<style>
    body {
      height: 100vh;
      max-height: 100vh;
      overflow: hidden;
      position: fixed;
    }
    .jspsych-content-wrapper {
      overflow: hidden;
    }
    </style>`;

    // Add card game wrap.
    new_html += '<div class="pit-game-wrap">';

    //
    new_html += '<div class="border" side="left"></div>';
    new_html += '<div class="border" side="right"></div>';

    // Iteratively draw cards.
    for (let i = 4; i > 0; i--) {

        // Start drawing card.
        new_html += `<div class="flip-card" id="card-${i}">`;
        new_html += `<div class="flip-card-inner">`;

        // Draw card front.
        new_html += `<div class="flip-card-front" valence="${trial.valence}">`;
        new_html += '<div class="background"></div>';
        // if ( i == 1 ) { new_html += `<img src="${trial.image}">`; }
        new_html += '</div>';

        if ( i == 1 ){

          // Start card back.
          new_html += `<div class="flip-card-back">`;
          new_html += '</div>';

        }

        // Finish card.
        new_html += '</div></div>';

    }

    // Close wrapper.
    new_html += '</div>';

    // draw HTML
    display_element.innerHTML = new_html;

    //---------------------------------------//
    // Response handling.
    //---------------------------------------//

    // store response
    var response = {
      rt: -1,
      key: -1
    };

    // function to handle responses by the subject
    var after_response = function(info) {

      // Kill any timeout handlers / keyboard listeners
      jsPsych.pluginAPI.clearAllTimeouts();
      jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);

      // Record response (if any made)
      if (info != null) {
        response = info;
      }

      // Define accuracy
      // if (trial.correct == response.key) {
      //   response.accuracy = 1;
      // } else {
      //   response.accuracy = 0;
      // };

      // Define outcome
      // if (response.accuracy == 1) {
      //   trial.outcome = trial.outcome_correct;
      // } else {
      //   trial.outcome = trial.outcome_incorrect;
      // }

      // Display card flip animation.
      if ( response.key >= 0 ) {
        document.getElementById(`card-1`).setAttribute('status', 'flip-right');
      } else {
        document.getElementById(`card-1`).setAttribute('status', 'flip-left');
      }

      jsPsych.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.feedback_duration);

    };

    // function to end trial when it is time
    var end_trial = function() {

      // Kill any timeout handlers / keyboard listeners
      jsPsych.pluginAPI.clearAllTimeouts();
      jsPsych.pluginAPI.cancelAllKeyboardResponses();
      if (typeof keyboardListener !== 'undefined') {
        jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
      }

      // gather the data to store for the trial
      var trial_data = {
        "valence": trial.valence,
        "key_press": response.key,
        "choice": response.choice,
        "rt": response.rt,
      };

      // clear the display
      display_element.innerHTML = '';

      // move on to the next trial
      jsPsych.finishTrial(trial_data);

    };

    // Start the response listener
    if (trial.valid_responses != jsPsych.NO_KEYS) {

      // Task keyboardListener
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
      }, trial.animation_duration + trial.choice_duration);
    }


  };

  return plugin;
})();
