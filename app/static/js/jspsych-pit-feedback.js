/**
 * jspsych-pit-feedback
 **/

jsPsych.plugins["pit-feedback"] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'pit-feedback',
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
      feedback_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Feedback duration',
        default: 1000,
        description: 'How long to show feedback before it ends.'
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
    new_html += `<style>
    body {
      background: -webkit-gradient(linear, left bottom, left top, from(#808080), color-stop(50%, #606060), color-stop(50%, rgba(28, 25, 23, 0.5)), to(rgba(179, 230, 230, 0.5)));
      background: linear-gradient(0deg, #808080 0%, #606060 50%, #A0A0A0 50%, #D3D3D3 100%);
      height: 100vh;
      max-height: 100vh;
      overflow: hidden;
      position: fixed;
    }
    .conveyor:after {-webkit-animation: none; animation: none;}
    .torso .rune { -webkit-animation: none; animation: action-cue none; }
    .window { -webkit-animation: none; animation: action-cue none; }
    </style>`;

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
    new_html += `<div class="rune"><img src="${trial.robot_rune}" style="height: 100%; width: 100%; object-fit: contain"></div></div>`;
    new_html += '<div class="foot"></div></div>';

    // Add factory window.
    new_html += `<div class="window" style="background: ${trial.scanner_color}"></div>`;

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
        "Duration": trial.feedback_duration,
        "Score": trial.score_post
      };

      // clear the display
      display_element.innerHTML = '';

      // move on to the next trial
      jsPsych.finishTrial(trial_data);
    };

    // end trial if feedback_duration is set
    if (trial.feedback_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.feedback_duration);
    }

  };

  return plugin;
})();
