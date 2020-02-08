/**
 * jspsych-pit-feedback
 **/

jsPsych.plugins["pit-feedback"] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'pit-feedback',
    description: '',
    parameters: {
      trial_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: 200,
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

    // Insert CSS (turn off conveyor animation).
    new_html += `<style>.conveyor:after {-webkit-animation: none; animation: none;}</style>`;

    // Add robot factor wrapper.
    new_html += '<div id="jspsych-pit-feedback-stimulus"><div class="wrap">';

    // Add factory machine parts (back).
    new_html += '<div class="machine-back"></div>';
    new_html += '<div class="conveyor"></div>';
    new_html += '<div class="shadows"></div>';

    // Add robot 1 (active).
    new_html += '<div class="robot" style="left: 50vw">';
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
    new_html += `<div class="machine-front"><div class="score-container"><div class="score">${trial.outcome}</div></div></div>`;
    new_html += '<div class="machine-top"></div>';
    new_html += '</div></div>';

    // Display HTML
    display_element.innerHTML = new_html;

    //---------------------------------------//
    // Response handling.
    //---------------------------------------//

    // function to end trial when it is time
    var end_trial = function() {

      // kill any remaining setTimeout handlers
      jsPsych.pluginAPI.clearAllTimeouts();

      // gather the data to store for the trial
      var trial_data = {
        "Duration": trial.duration,
        "Score": trial.score_post
      };

      // clear the display
      display_element.innerHTML = '';

      // move on to the next trial
      jsPsych.finishTrial(trial_data);
    };

    // end trial if trial_duration is set
    if (trial.trial_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.trial_duration);
    }

  };

  return plugin;
})();
