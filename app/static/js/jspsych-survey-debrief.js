/**
 * jspsych-survey-debrief
 */

jsPsych.plugins['survey-debrief'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'survey-debrief',
    description: '',
    parameters: {
      button_label: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button label',
        default:  'Continue',
        description: 'The text that appears on the button to finish the trial.'
      },
    }
  }
  plugin.trial = function(display_element, trial) {

    //---------------------------------------//
    // Define HTML.
    //---------------------------------------//

    // Initialize HTML
    var html = '';

    // Inject CSS
    html += `<style>
    .wrap {
      height: 100vh;
      width: 100vw;
    }
    .debrief-header {
      margin: auto;
      top: 5%;
      width: 100%;
      padding: 0 0 0 0;
      background-color: #fff;
      font-size: 90%;
      text-align: center;
    }
    .debrief-footer {
      margin: auto;
      top: 95%;
      width: 100%;
      padding: 0 0 0 0;
      background-color: #fff;
      text-align: right;
    }
    input[type=text], select, textarea{
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    input[type=number], select, textarea{
      padding: 4px 12px;
      border: 1px solid #ccc;
      border-radius: 4px;
      width: 60px;
    }
    input[type="radio"] {
      margin: 0 6px 0 0;
    }
    input[type="checkbox"] {
      margin: 0 6px 0 0;
    }
    label {
      padding: 0 8px 0 0;
      display: inline-block;
    }
    .debrief-footer input[type=submit] {
      background-color: #ffb347;
      color: white;
      padding: 8px 20px;
      border: none;
      border-radius: 4px;
      float: right;
      margin-top: 2px;
      margin-right: -15px;
      margin-bottom: 20px;
    }
    .container {
      margin: auto;
      width: 100%;
      background-color: #F8F8F8;
      padding: 5px 0 5px 15px;
      border-radius: 5px;
    }
    .debrief-prompt {
      float: left;
      width: 33%;
      margin-top: 6px;
      margin-bottom: 6px;
      font-size: 90%;
      text-align: left;
    }
    .debrief-resp {
      float: left;
      width: 66%;
      margin-top: 6px;
      margin-bottom: 6px;
      font-size: 85%;
      text-align: left;
    }
    .row:after {
      content: "";
      display: table;
      clear: both; }
    @media screen and (max-width: 600px) {
      .debrief-prompt, .debrief-resp, input[type=submit] {
        width: 100%;
        margin-top: 0;
      }
    };
    </style>`;

    // Add debriefing header.
    html += '<div class=header>';
    html += '<h2>Debriefing</h2>';
    html += '<p>Please answer the questions below. <font color="#c87606">Your answers will not affect your payment or bonus.</font></p>'
    html += '</div>';

    // Begin form
    html += '<form id="jspsych-survey-debrief">'

    // Add debriefing form
    html += '<div class="container">';

    // Item 1: Task difficulty
    html += '<div class="row">';
    html += '<div class="debrief-prompt"><label for="country">How difficult was the task?</label></div>';
    html += '<div class="debrief-resp">';
    html += '<label><input type="radio" name="difficulty" value="1" required>Very easy</label><br>';
    html += '<label><input type="radio" name="difficulty" value="2" required>Somewhat easy</label><br>';
    html += '<label><input type="radio" name="difficulty" value="3" required>Neither easy nor hard</label><br>';
    html += '<label><input type="radio" name="difficulty" value="4" required>Somewhat hard</label><br>';
    html += '<label><input type="radio" name="difficulty" value="5" required>Very hard</label>';
    html += '</div></div>';
    html += '<hr color="#fff">';

    // Item 2: Task enjoyment
    html += '<div class="row">';
    html += '<div class="debrief-prompt"><label for="country">How fun was the task?</label></div>';
    html += '<div class="debrief-resp">';
    html += '<label><input type="radio" name="fun" value="1" required>Very fun</label><br>';
    html += '<label><input type="radio" name="fun" value="2" required>Somewhat fun</label><br>';
    html += '<label><input type="radio" name="fun" value="3" required>Neither fun nor boring</label><br>';
    html += '<label><input type="radio" name="fun" value="4" required>Somewhat boring</label><br>';
    html += '<label><input type="radio" name="fun" value="5" required>Very boring</label>';
    html += '</div></div>';
    html += '<hr color="#fff">';

    // Item 3: Instructions clarity
    html += '<div class="row">';
    html += '<div class="debrief-prompt"><label for="country">How clear were the instructions?</label></div>';
    html += '<div class="debrief-resp">';
    html += '<label><input type="radio" name="clarity" value="1" required>Very clear</label><br>';
    html += '<label><input type="radio" name="clarity" value="2" required>Somewhat clear</label><br>';
    html += '<label><input type="radio" name="clarity" value="3" required>Neither clear nor confusing</label><br>';
    html += '<label><input type="radio" name="clarity" value="4" required>Somewhat confusing</label><br>';
    html += '<label><input type="radio" name="clarity" value="5" required>Very confusing</label>';
    html += '</div></div>';
    html += '<hr color="#fff">';

    // Item 4: Task strategies
    html += '<div class="row">';
    html += '<div class="debrief-prompt"><label for="strategy">Did you use any strategies during the task (e.g. write things down)?</label></div>';
    html += '<div class="debrief-resp"><input type="text" name="strategy" size="40"></div>';
    html += '</div>';
    html += '<hr color="#fff">';

    // Item 5: Additional comments.
    html += '<div class="row">';
    html += '<div class="debrief-prompt"><label for="feedback">Do you have any other comments?</label></div>';
    html += '<div class="debrief-resp"><input type="text" name="feedback" size="40"></div>';
    html += '</div>';

    // Close container.
    html += '</div>';

    // Add submit button.
    html += '<div class="debrief-footer">';
    html += `<input type="submit" id="jspsych-survey-debrief-next" class="jspsych-btn jspsych-survey-debrief" value="${trial.button_label}"></input>`;
    html += '</div>';

    // End form
    html += '</form>'

    // Display HTML
    display_element.innerHTML = html;

    //---------------------------------------//
    // Define functions.
    //---------------------------------------//

    // scroll to top of screen
    window.scrollTo(0,0);

    display_element.querySelector('#jspsych-survey-debrief').addEventListener('submit', function(event) {

        // Wait for response
        event.preventDefault();

        // verify that at least one box has been checked for the race question
        var checkboxes = document.querySelectorAll('input[type="checkbox"]');

          // Measure response time
          var endTime = performance.now();
          var response_time = endTime - startTime;

          var question_data = serializeArray(this);
          question_data = objectifyForm(question_data);

          // Store data
          var trialdata = {
            "rt": response_time,
            "debriefgraphics": question_data
          };

          // Update screen
          display_element.innerHTML = '';

          // Move onto next trial
          jsPsych.finishTrial(trialdata);

    });

    var startTime = performance.now();

  };

  /*!
   * Serialize all form data into an array
   * (c) 2018 Chris Ferdinandi, MIT License, https://gomakethings.com
   * @param  {Node}   form The form to serialize
   * @return {String}      The serialized form data
   */
  var serializeArray = function (form) {
    // Setup our serialized data
    var serialized = [];

    // Loop through each field in the form
    for (var i = 0; i < form.elements.length; i++) {
      var field = form.elements[i];

      // Don't serialize fields without a name, submits, buttons, file and reset inputs, and disabled fields
      if (!field.name || field.disabled || field.type === 'file' || field.type === 'reset' || field.type === 'submit' || field.type === 'button') continue;

      // If a multi-select, get all selections
      if (field.type === 'select-multiple') {
        for (var n = 0; n < field.options.length; n++) {
          if (!field.options[n].selected) continue;
          serialized.push({
            name: field.name,
            value: field.options[n].value
          });
        }
      }

      // Convert field data to a query string
      else if ((field.type !== 'checkbox' && field.type !== 'radio') || field.checked) {
        serialized.push({
          name: field.name,
          value: field.value
        });
      }
    }

    return serialized;
  };

  // from https://stackoverflow.com/questions/1184624/convert-form-data-to-javascript-object-with-jquery
  function objectifyForm(formArray) {//serialize data function
    var returnArray = {};
    for (var i = 0; i < formArray.length; i++){
      returnArray[formArray[i]['name']] = formArray[i]['value'];
    }
    return returnArray;
  }

  return plugin;

})();
