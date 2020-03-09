/**
 * jspsych-survey-demo
 * a jspsych plugin for the Niv lab demographics form
 */

jsPsych.plugins['survey-demo'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'survey-demo',
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

    // scroll to top of screen
    window.scrollTo(0,0);

    // Initialize HTML
    var html = '';

    // Inject CSS
    html += '<style>';
    html += '.demo-header { margin: auto; top: 5%; width: 100%; padding: 0 0 0 0; background-color: #fff; font-size: 90%; text-align: center; }'+
      '.demo-footer { margin: auto; top: 95%; width: 100%; padding: 0 0 0 0; background-color: #fff; text-align: right; }'+
      'input[type=text], select, textarea{ border: 1px solid #ccc; border-radius: 4px; }'+
      'input[type=number], select, textarea{ padding: 4px 12px; border: 1px solid #ccc; border-radius: 4px; width: 60px; }'+
      'input[type="radio"] { margin: 0 6px 0 0; }'+
      'input[type="checkbox"] { margin: 0 6px 0 0; }'+
      'label { padding: 0 8px 0 0; display: inline-block; }'+
      '.demo-footer input[type=submit] { background-color: #ffb347; color: white; padding: 8px 20px; border: none; border-radius: 4px; float: right; margin-top: 2px; margin-right: -15px; margin-bottom: 20px; }'+
      '.container { margin: auto; width: 100%; background-color: #F8F8F8; padding: 5px 0 5px 15px; border-radius: 5px; }'+
      '.demo-prompt { float: left; width: 33%; margin-top: 6px; margin-bottom: 6px; font-size: 90%; text-align: left; }'+
      '.demo-resp { float: left; width: 66%; margin-top: 6px; margin-bottom: 6px; font-size: 85%; text-align: left; }'+
      '.row:after { content: ""; display: table; clear: both; }'+
      '@media screen and (max-width: 600px) { .demo-prompt, .demo-resp, input[type=submit] { width: 100%; margin-top: 0; } }';
    html += '</style>';

    // Add header
    html += `
    <div class=demo-header><h2>Demographics Survey</h2>
        <p>Please answer the questions below. <font color="#c87606">Your answers will not affect your payment or bonus.</font></p>
    </div>`

    // Begin form
    html += '<form id="jspsych-survey-demo">'

    // Add demographics form
    html += `
    <div class="container">

    		<div class="row">

    				<div class="demo-prompt">
    						<label for="age">What is your age?</label>
    				</div>

    				<div class="demo-resp">
    						<input type="number" name="age" min="18" max="100" size="20">
    				</div>
    		</div>

    		<hr color="#fff">

    		<div class="row">

    				<div class="demo-prompt">
    						<label for="country">What is your gender?</label>
    				</div>

    				<div class="demo-resp">
                <label><input type="radio" name="gender-categorical" value="Male" required>Male</label>
                <label><input type="radio" name="gender-categorical" value="Female" required>Female</label>
                <label><input type="radio" name="gender-categorical" value="Rather not say" required>Rather not say</label>
                <label><input type="radio" name="gender-categorical" value="Other" required>Other</label>
    				</div>

    		</div>

    		<hr color="#fff">

    		<div class="row">

    				<div class="demo-prompt">
    						<label for="country">What is your ethnicity?</label>
    				</div>

    				<div class="demo-resp">
    						<label><input type="radio" name="ethnicity" value="Hispanic or Latino" required>Hispanic or Latino</label><br>
    						<label><input type="radio" name="ethnicity" value="Not Hispanic or Latino" required>Not Hispanic or Latino</label><br>
    						<label><input type="radio" name="ethnicity" value="Unknown" required>Unknown</label><br>
    						<label><input type="radio" name="ethnicity" value="Rather not say" required>Rather not say</label>
    				</div>

    		</div>

    		<hr color="#fff">

    		<div class="row">

    				<div class="demo-prompt">
    						<label for="country">		What is your race?<br><small>(Choose all that apply)</small></label>
    				</div>

    				<div class="demo-resp">
    						<label><input type="checkbox" name="race" value="American Indian/Alaska Native">American Indian/Alaska Native</label><br>
    						<label><input type="checkbox" name="race" value="Asian">Asian</label><br>
    						<label><input type="checkbox" name="race" value="Native Hawaiian or other Pacific Islander">Native Hawaiian or other Pacific Islander</label><br>
    						<label><input type="checkbox" name="race" value="Black or African American">Black or African American</label><br>
    						<label><input type="checkbox" name="race" value="White">White</label><br>
    						<label><input type="checkbox" name="race" value="Rather not say">Rather not say</label>
    				</div>

    		</div>

    		<hr color="#fff">

    		<div class="row">

    				<div class="demo-prompt">
    						<label for="english">Is English your first language?</label>
    				</div>

    				<div class="demo-resp">
    						<label><input type="radio" name="english" value="Yes" required>Yes</label>
    						<label><input type="radio" name="english" value="No" required>No</label>
    				</div>

    		</div>

    		<hr color="#fff">

    		<div class="row">

    				<div class="demo-prompt">
    						<label for="fluency">How well do you speak English?</label>
    				</div>

    				<div class="demo-resp">
    						<label><input type="radio" name="fluency" value="Very well" required>Very well</label>
    						<label><input type="radio" name="fluency" value="Well" required>Well</label>
    						<label><input type="radio" name="fluency" value="Not well" required>Not well</label>
    						<label><input type="radio" name="fluency" value="Not at all" required>Not at all</label>
    				</div>

    		</div>

    </div>`

    // Add submit button
    html += `
    <div class="demo-footer">
        <input type="submit" id="jspsych-survey-demo-next" class="jspsych-btn jspsych-survey-demo" value="${trial.button_label}"></input>
    </div>`;

    // End form
    html += '</form>'

    // Display HTML
    display_element.innerHTML = html;

    display_element.querySelector('#jspsych-survey-demo').addEventListener('submit', function(event) {

        // Wait for response
        event.preventDefault();

        // verify that at least one box has been checked for the race question
        var checkboxes = document.querySelectorAll('input[type="checkbox"]');
        var checkedOne = Array.prototype.slice.call(checkboxes).some(x => x.checked);

        if(!checkedOne){

          alert("You did not enter a response for the question \"What is your race?\". Please choose at least one option.");

        } else {

          // Measure response time
          var endTime = performance.now();
          var response_time = endTime - startTime;

          var question_data = serializeArray(this);
          question_data = objectifyForm(question_data);

          // Store data
          var trialdata = {
            "rt": response_time,
            "demographics": question_data
          };

          // Update screen
          display_element.innerHTML = '';

          // Move onto next trial
          jsPsych.finishTrial(trialdata);

        }



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
