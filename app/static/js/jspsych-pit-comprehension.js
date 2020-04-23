/**
 * jspsych-pit-comprehension
 * Sam Zorowitz
 *
 * plugin for running the comprehension check for the PIT task
 *
 **/

jsPsych.plugins['pit-comprehension'] = (function() {
  var plugin = {};

  plugin.info = {
    name: 'pit-comprehension',
    description: '',
    parameters: {
      button_label: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button label',
        default:  'Continue',
        description: 'Label of the button.'
      },
      win_color_text: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Win color name',
        default:  'black',
        description: 'Name of the win color.'
      },
      loss_color_text: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Loss color name',
        default:  'black',
        description: 'Name of the loss color.'
      },
      win_color_hex: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Win color hex',
        default:  'black',
        description: 'Hex code of the win color.'
      },
      loss_color_hex: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Loss color hex',
        default:  'black',
        description: 'Hex code of the loss color.'
      }
    }
  }
  plugin.trial = function(display_element, trial) {

    // Plug-in setup
    var plugin_id_name = "jspsych-survey-multi-choice";
    var plugin_id_selector = '#' + plugin_id_name;
    var _join = function( /*args*/ ) {
      var arr = Array.prototype.slice.call(arguments, _join.length);
      return arr.join(separator = '-');
    }

    // ---------------------------------- //
    // Section 1: Define Prompts          //
    // ---------------------------------- //

    // Define comprehension check questions.
    var prompts = [
      "To reject a robot (i.e. judge as incomplete), what do you do?",
      `When the scanner light is <b><font color=${trial.win_color_hex}>${trial.win_color_text}</font></b>, how many points will you earn for a correct judgment?`,
      `When the scanner light is <b><font color=${trial.lose_color_hex}>${trial.lose_color_text}</font></b>, how many points will you earn for a correct judgment?`,
      "<i>True</i> or <i>False</i>: the scanner will sometimes malfunction and provide incorrect feedback.",
      "Will the number of points I earn affect my performance bonus?"
    ];

    // Define response options.
    var options = [
      ["Press SPACE", "Do nothing", "Press ENTER"],
      ["+10", "+1", "-1", "-10"],
      ["+10", "+1", "-1", "-10"],
      ["True", "False"],
      ["Yes" ,"No"]
    ];

    // Define correct answers.
    var correct = [
      "Do nothing",
      "+10",
      "-1",
      "True",
      "Yes"
    ]

    // ---------------------------------- //
    // Section 2: Define HTML             //
    // ---------------------------------- //

    // Initialize HTML
    var html = "";

    // Initialize HTML
    var html = "";

    // inject CSS for trial
    html += `<style>
    body {
      background: -webkit-gradient(linear, left bottom, left top, from(#808080), color-stop(50%, #606060), color-stop(50%, rgba(28, 25, 23, 0.5)), to(rgba(179, 230, 230, 0.5)));
      background: linear-gradient(0deg, #808080 0%, #606060 50%, #A0A0A0 50%, #D3D3D3 100%);
      height: 100vh;
      max-height: 100vh;
      overflow: hidden;
      position: fixed;
    }
    .conveyor:after {-webkit-animation: none; animation: none;}
     </style>`;

    // Add factory machine parts (back).
    html += '<div class="factory-wrap">';
    html += '<div class="machine-back"></div>';
    html += '<div class="conveyor"></div>';
    html += '<div class="shadows"></div>';
    html += `<div class="machine-front"></div>`;
    html += '<div class="machine-top"></div>';

    // form element
    var trial_form_id = _join(plugin_id_name, "form");
    display_element.innerHTML += '<form id="'+trial_form_id+'"></form>';

    // Show preamble text
    html += '<div class="comprehension-box">'
    html += '<div class="jspsych-survey-multi-choice-preamble"><h4>Please answer the questions below:</h4></div>';

    // Initialize form element
    html += '<form id="jspsych-survey-multi-choice-form">';

    // Iteratively add comprehension questions.
    for (i = 0; i < prompts.length; i++) {

      // Initialize item
      html += `<div id="jspsych-survey-multi-choice-${i}" class="jspsych-survey-multi-choice-question jspsych-survey-multi-choice-horizontal" data-name="Q${i}">`;

      // Add question text
      html += `<p class="jspsych-survey-multi-choice-text survey-multi-choice">${prompts[i]}</p>`;

      // Iteratively add options.
      for (j = 0; j < options[i].length; j++) {

        // Option 1: True
        html += `<div id="jspsych-survey-multi-choice-option-${i}-${j}" class="jspsych-survey-multi-choice-option">`;
        html += `<input type="radio" name="jspsych-survey-multi-choice-response-${i}" id="jspsych-survey-multi-choice-response-${i}-${j}" value="${options[i][j]}" required>`;
        html += `<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-${i}-${j}">${options[i][j]}</label>`;
        html += '</div>';

      }

      // Close item
      html += '<br></div>';

    }

    // add submit button
    html += '<input type="submit" id="'+plugin_id_name+'-next" class="'+plugin_id_name+' jspsych-btn"' + (trial.button_label ? ' value="'+trial.button_label + '"': '') + '"></input>';

    // End HTML
    html += '</form>';
    html += '</div></div>';

    // Display HTML
    display_element.innerHTML = html;

    // ---------------------------------- //
    // Section 2: jsPsych Functions       //
    // ---------------------------------- //

    // Detect submit button press
    document.querySelector('form').addEventListener('submit', function(event) {
      event.preventDefault();

      // Measure response time
      var endTime = performance.now();
      var response_time = endTime - startTime;

      // Gather responses
      var responses = [];
      var num_errors = 0;
      for (var i=0; i<prompts.length; i++) {

        // Find matching question.
        var match = display_element.querySelector('#jspsych-survey-multi-choice-'+i);
        var val = match.querySelector("input[type=radio]:checked").value;

        // Store response
        responses.push(val)

        // Check accuracy
        if ( correct[i] != val ) {
          num_errors++;
        }

      }

      // store data
      var trial_data = {
        "responses": responses,
        "num_errors": num_errors,
        "rt": response_time
      };

      // clear html
      display_element.innerHTML += '';

      // next trial
      jsPsych.finishTrial(trial_data);

    });

    var startTime = performance.now();
  };

  return plugin;
})();
