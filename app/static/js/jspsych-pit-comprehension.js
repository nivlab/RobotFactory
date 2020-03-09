/**
* jspsych-pit-comprehension
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
    // Section 1: Define HTML             //
    // ---------------------------------- //

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
    .comprehension-box {
      position: absolute;
      top: 50%;
      left: 50%;
      -webkit-transform: translate3d(-50%, -65%, 0);
      transform: translate3d(-50%, -65%, 0);
      width: 70vh;
      height: 50vh;
      background: #ffffff;
      border: 2px solid black;
      border-radius: 12px;
      line-height: 1.15em;
    }
    .jspsych-survey-multi-choice-question {
      margin-top: 0em;
      margin-bottom: 1.0em;
      text-align: left;
      padding-left: 2em;
      font-size: 1.5vh;
    }
    .jspsych-survey-multi-choice-horizontal .jspsych-survey-multi-choice-text {
      text-align: left;
      margin: 0em 0em 0em 0em
    }
    .jspsych-survey-multi-choice-horizontal .jspsych-survey-multi-choice-option {
      display: inline-block;
      margin: 0em 1em 0em 1em;
    }
    .jspsych-survey-multi-choice-option input[type='radio'] {
      margin-right: 0.5em;
      width: 1em;
      height: 1em;
    }
    .invalid {
      display:inline-block;
      border: 1px solid;
      border-radius: 4px;
      margin: 0.25em 1em 0em 1em;
      padding: 0px 4px 0px 4px;
      color: #D8000C;
      background-color: #FFBABA;
      font-size: 1.25vh;
      animation: flash 0.1s;
      -webkit-animation: flash 0.1s;
    }
    .valid {
      display: none
    }
    @keyframes flash {
      from { opacity: 50%; }
      to { opacity: 100%; }
    }
    @-webkit-keyframes flash {
      from { opacity: 50%; }
      to { opacity: 100%; }
    }
    .conveyor:after {-webkit-animation: none; animation: none;}
     </style>`;

    // Add factory machine parts (back).
    html += '<div class="wrap">';
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
    html += '<div class="jspsych-survey-multi-choice-preamble"><h4 style="font-size: 2vh; margin-block-start: 0.5em; margin-block-end: 0.5em">Please answer the questions below:</div>';

    // Initialize form element
    html += '<form id="jspsych-survey-multi-choice-form">';

    // add submit button
    html += '<input type="submit" id="'+plugin_id_name+'-next" class="'+plugin_id_name+' jspsych-btn"' + (trial.button_label ? ' value="'+trial.button_label + '"': '') + 'style="position: absolute; top: 95%; left: 50%; -webkit-transform: translate3d(-50%, -50%, 0); transform: translate3d(-50%, -50%, 0); font-size: 1.25vh" disabled></input>';

    // ---------------------------------- //
    // Comprehension Question #1          //
    // ---------------------------------- //

    // Initialize item
    html += '<div id="jspsych-survey-multi-choice-0" class="jspsych-survey-multi-choice-question jspsych-survey-multi-choice-horizontal" data-name="no-press">';

    // Add question text
    html += '<p class="jspsych-survey-multi-choice-text survey-multi-choice">To reject a robot (i.e. judge as incomplete), what do you do?</p>';

    // Option 1: Press SPACE
    html += '<div id="jspsych-survey-multi-choice-option-0-0" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-0" id="jspsych-survey-multi-choice-response-0-0" value="Press SPACE" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-0-0">Press SPACE</label>';
    html += '</div>';

    // Option 2: Do nothing
    html += '<div id="jspsych-survey-multi-choice-option-0-1" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-0" id="jspsych-survey-multi-choice-response-0-1" value="Do nothing" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-0-1">Do nothing</label>';
    html += '</div>';

    // Option 3: Press enter
    html += '<div id="jspsych-survey-multi-choice-option-0-2" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-0" id="jspsych-survey-multi-choice-response-0-2" value="Press ENTER" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-0-2">Press ENTER</label>';
    html += '</div>';

    // Close item
    html += '<br><p class="error" id="Q1-error"></p>'
    html += '</div>';

    // ---------------------------------- //
    // Comprehension Question #2          //
    // ---------------------------------- //

    // Initialize item
    html += '<div id="jspsych-survey-multi-choice-1" class="jspsych-survey-multi-choice-question jspsych-survey-multi-choice-horizontal" data-name="probability">';

    // Add question text
    html += '<p class="jspsych-survey-multi-choice-text survey-multi-choice">When the scanner light is <b><font color=#006600>green</font></b>, how many points will you earn for a correct judgment?</p>';

    // Option 1: More likely
    html += '<div id="jspsych-survey-multi-choice-option-1-0" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-1" id="jspsych-survey-multi-choice-response-1-0" value="1" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-1-0">1</label>';
    html += '</div>';

    // Option 2: Less likely
    html += '<div id="jspsych-survey-multi-choice-option-1-1" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-1" id="jspsych-survey-multi-choice-response-1-1" value="0" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-1-1">0</label>';
    html += '</div>';

    // Option 3: Equally likely
    html += '<div id="jspsych-survey-multi-choice-option-1-2" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-1" id="jspsych-survey-multi-choice-response-1-2" value="-1" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-1-2">-1</label>';
    html += '</div>';

    // Close item
    html += '<br><p id="Q2-error"></p>'
    html += '</div>';

    // ---------------------------------- //
    // Comprehension Question #3          //
    // ---------------------------------- //

    // Initialize item
    html += '<div id="jspsych-survey-multi-choice-2" class="jspsych-survey-multi-choice-question jspsych-survey-multi-choice-horizontal" data-name="probability">';

    // Add question text
    html += '<p class="jspsych-survey-multi-choice-text survey-multi-choice">When the scanner light is <b><font color=#b30000>red</font></b>, how many points will you earn for a correct judgment?</p>';

    // Option 1: More likely
    html += '<div id="jspsych-survey-multi-choice-option-2-0" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-2" id="jspsych-survey-multi-choice-response-2-0" value="1" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-2-0">1</label>';
    html += '</div>';

    // Option 2: Less likely
    html += '<div id="jspsych-survey-multi-choice-option-2-1" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-2" id="jspsych-survey-multi-choice-response-2-1" value="0" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-2-1">0</label>';
    html += '</div>';

    // Option 3: Equally likely
    html += '<div id="jspsych-survey-multi-choice-option-2-2" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-2" id="jspsych-survey-multi-choice-response-2-2" value="-1" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-2-2">-1</label>';
    html += '</div>';

    // Close item
    html += '<br><p id="Q3-error"></p>'
    html += '</div>';

    // ---------------------------------- //
    // Comprehension Question #4          //
    // ---------------------------------- //

    // Initialize item
    html += '<div id="jspsych-survey-multi-choice-3" class="jspsych-survey-multi-choice-question jspsych-survey-multi-choice-horizontal" data-name="bonus">';

    // Add question text
    html += '<p class="jspsych-survey-multi-choice-text survey-multi-choice"><i>True</i> or <i>False</i>: the scanner will sometimes malfunction and provide incorrect feedback.</p>';

    // Option 1: Yes
    html += '<div id="jspsych-survey-multi-choice-option-3-0" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-3" id="jspsych-survey-multi-choice-response-3-0" value="True" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-3-0">True</label>';
    html += '</div>';

    // Option 2: No
    html += '<div id="jspsych-survey-multi-choice-option-3-1" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-3" id="jspsych-survey-multi-choice-response-3-1" value="False" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-3-1">False</label>';
    html += '</div>';

    // Close item
    html += '<br><p id="Q4-error"></p>'
    html += '</div>';

    // ---------------------------------- //
    // Comprehension Question #5          //
    // ---------------------------------- //

    // Initialize item
    html += '<div id="jspsych-survey-multi-choice-4" class="jspsych-survey-multi-choice-question jspsych-survey-multi-choice-horizontal" data-name="bonus">';

    // Add question text
    html += '<p class="jspsych-survey-multi-choice-text survey-multi-choice">Will the number of points I earn affect performance bonus?</p>';

    // Option 1: Yes
    html += '<div id="jspsych-survey-multi-choice-option-4-0" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-4" id="jspsych-survey-multi-choice-response-4-0" value="Yes" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-4-0">Yes</label>';
    html += '</div>';

    // Option 2: No
    html += '<div id="jspsych-survey-multi-choice-option-4-1" class="jspsych-survey-multi-choice-option">';
    html += '<input type="radio" name="jspsych-survey-multi-choice-response-4" id="jspsych-survey-multi-choice-response-4-1" value="No" required>';
    html += '<label class="jspsych-survey-multi-choice-text" for="jspsych-survey-multi-choice-response-4-1">No</label>';
    html += '</div>';

    // Close item
    html += '<br><p id="Q5-error"></p>'
    html += '</div>';

    // End HTML
    html += '</form>';
    html += '</div></div>';

    // Display HTML
    display_element.innerHTML = html;

    // ---------------------------------- //
    // Section 2: jsPsych Functions       //
    // ---------------------------------- //

    // Define error messages
    const Q1 = document.getElementById("Q1-error");
    const Q2 = document.getElementById("Q2-error");
    const Q3 = document.getElementById("Q3-error");
    const Q4 = document.getElementById("Q4-error");
    const Q5 = document.getElementById("Q5-error");
    var count = 0;

    // Detect changes on first comprehension item
    display_element.querySelector('#jspsych-survey-multi-choice-0').addEventListener('change', function(){

      // On change, find which item is checked.
      var val = display_element.querySelector('#jspsych-survey-multi-choice-0 input:checked').value;

      // Validation
      if (val === "Do nothing") {

        // Update text
        Q1.innerHTML = "";
        Q1.className = "valid"

      } else {

        // Update text
        Q1.innerHTML = "That's incorrect. Hint: To reject a robot, don't press any button.";
        Q1.className = "invalid"

        // Restart animation
        Q1.style.animation = 'none';
        Q1.offsetHeight; /* trigger reflow */
        Q1.style.animation = null;

        // Increment error count
        count += 1;

      }

    });

    // Detect changes on second comprehension item
    display_element.querySelector('#jspsych-survey-multi-choice-1').addEventListener('change', function(){

      // On change, find which item is checked.
      var val = display_element.querySelector('#jspsych-survey-multi-choice-1 input:checked').value;

      // Validation
      if (val === "1") {

        // Update text
        Q2.innerHTML = "";
        Q2.className = "valid"

      } else {

        // Update text
        Q2.innerHTML = "That's incorrect. Hint: When the light is green you can earn either 1 or 0 points.";
        Q2.className = "invalid"

        // Restart animation
        Q2.style.animation = 'none';
        Q2.offsetHeight; /* trigger reflow */
        Q2.style.animation = null;

        // Increment error count
        count += 1;

      }

    });

    // Detect changes on second comprehension item
    display_element.querySelector('#jspsych-survey-multi-choice-2').addEventListener('change', function(){

      // On change, find which item is checked.
      var val = display_element.querySelector('#jspsych-survey-multi-choice-2 input:checked').value;

      // Validation
      if (val === "0") {

        // Update text
        Q3.innerHTML = "";
        Q3.className = "valid"

      } else {

        // Update text
        Q3.innerHTML = "That's incorrect. Hint: When the light is red you can earn 0 or -1 points.";
        Q3.className = "invalid"

        // Restart animation
        Q3.style.animation = 'none';
        Q3.offsetHeight; /* trigger reflow */
        Q3.style.animation = null;

        // Increment error count
        count += 1;

      }

    });

    // Detect changes on third comprehension item
    display_element.querySelector('#jspsych-survey-multi-choice-3').addEventListener('change', function(){

      // On change, find which item is checked.
      var val = display_element.querySelector('#jspsych-survey-multi-choice-3 input:checked').value;

      // Validation
      if (val === "True") {

        // Update text
        Q4.innerHTML = "";
        Q4.className = "valid"

      } else {

        // Update text
        Q4.innerHTML = "That's incorrect. The scanner will sometimes provide incorrect feedback.";
        Q4.className = "invalid"

        // Restart animation
        Q4.style.animation = 'none';
        Q4.offsetHeight; /* trigger reflow */
        Q4.style.animation = null;

        // Increment error count
        count += 1;

      }

    })


    // Detect changes on third comprehension item
    display_element.querySelector('#jspsych-survey-multi-choice-4').addEventListener('change', function(){

      // On change, find which item is checked.
      var val = display_element.querySelector('#jspsych-survey-multi-choice-4 input:checked').value;

      // Validation
      if (val === "Yes") {

        // Update text
        Q5.innerHTML = "";
        Q5.className = "valid"

      } else {

        // Update text
        Q5.innerHTML = "That's incorrect. Your bonus will reflect your performance on the task.";
        Q5.className = "invalid"

        // Restart animation
        Q5.style.animation = 'none';
        Q5.offsetHeight; /* trigger reflow */
        Q5.style.animation = null;

        // Increment error count
        count += 1;

      }

    })

    // Detect if all correct answers
    display_element.addEventListener('change', function(){
      if (Q1.className === 'valid' && Q2.className === 'valid' && Q3.className === 'valid' && Q4.className === 'valid' && Q5.className === 'valid') {
        document.getElementById("jspsych-survey-multi-choice-next").disabled = false;
      } else {
        document.getElementById("jspsych-survey-multi-choice-next").disabled = true;
      }
    })

    // Detect submit button press
    document.querySelector('form').addEventListener('submit', function(event) {
      event.preventDefault();

      // Measure response time
      var endTime = performance.now();
      var response_time = endTime - startTime;

      // Gather responses
      var question_data = {};
      for (var i=0; i<4; i++) {

        // Find matching question.
        var match = display_element.querySelector('#jspsych-survey-multi-choice-'+i);
        var name = match.attributes['data-name'].value;
        var val = match.querySelector("input[type=radio]:checked").value;

        // Store response
        var obje = {};
        obje[name] = val;
        Object.assign(question_data, obje);

      }

      // Save data
      var trial_data = {
        "rt": response_time,
        "responses": JSON.stringify(question_data),
        "errors": count
      };
      display_element.innerHTML += '';

      // next trial
      jsPsych.finishTrial(trial_data);
    });

    var startTime = performance.now();
  };

  return plugin;
})();
