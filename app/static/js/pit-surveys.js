//------------------------------------//
// Define transition screens.
//------------------------------------//

// Welcome screen
var WELCOME = {
  type: 'instructions',
  pages: [
    "<b>Welcome to the experiment!</b><br><br>We will get started with some surveys.<br>Please read each survey carefully and respond truthfully."
  ],
  show_clickable_nav: true,
  button_label_previous: 'Prev',
  button_label_next: 'Next',
  on_finish: function(trial) {
    pass_message('starting surveys');
  }
}

//------------------------------------//
// Define questionnaires.
//------------------------------------//

// Demographics questionnaire
var DEMO = {
  type: 'survey-demo',
  data: {survey: 'demographics'}
};

// Debriefing questionnaire
var DEBRIEF = {
  type: 'survey-debrief',
  data: {survey: 'debrief'}
}

// Affective slider stimuli (NOTE: must be in this order).
var slider_stimuli = [
  '../static/img/slider_track.png',
  '../static/img/AS_intensity_cue.png',
  '../static/img/AS_unhappy.png',
  '../static/img/AS_happy.png',
  '../static/img/AS_sleepy.png',
  '../static/img/AS_wideawake.png',
  '../static/img/slider_thumb_selected.png',
  '../static/img/slider_thumb_unselected.png'
];

// Affective slider
var slider = {
  type: 'affective-slider',
  prompt: 'Please rate your current mood from completely sad (left) to completely happy (right).',
  slider_type: 'valence',
  left_anchor: 2, // indexes into the AS_stimuli array
  right_anchor: 3, // indexes into the AS_stimuli array
  AS_stimuli: slider_stimuli,
  initial_silent_duration: 500,
  initial_blank_duration: 0
}

// Generalized Anxiety Disorder Scale (GAD-7)
var gad7 = {
  type: 'survey-template',
  items: [

    // General anxiety
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it's hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid as if something awful might happen",

    // Infrequency item
    "Worrying too much about the 1983 World Cup"

  ],
  scale: [
    "Not at all",
    "Several days",
    "Over half the days",
    "Nearly every day"
  ],
  reverse: [
    false, false, false, false, false, false, false, false
  ],
  instructions: 'Over the <b>last 2 weeks</b>, how often have you been bothered by the following problems?',
  survey_width: 950,
  item_width: 40,
  infrequency_items: [7],
  data: {survey: 'gad7'},
  on_finish: function(data) {

    // Score response on infrequncy item.
    const scores = [0,1,1,1];
    data.infrequency = scores[data.responses['Q08']];

  }
}

// Depression, anxiety, and stress scale (DASS)
var dass = {
  type: 'survey-template',
  items: [

    // Depression subscale
    "I couldn't seem to experience any positive feeling at all.",
    "I found it difficult to work up the initiative to do things.",
    "I felt that I had nothing to look forward to.",
    "I felt down-hearted and blue.",
    "I was unable to become enthusiastic about anything.",
    "I felt I wasn't worth much as a person.",
    "I felt that life was meaningless.",

    // Infrequency item
    "I was able to remember my own name."

  ],
  scale: [
    "Never",
    "Sometimes",
    "Often",
    "Almost always"
  ],
  instructions: 'Please read each statement and indicate how much the statement applied to you <b>over the past week.</b>',
  survey_width: 950,
  item_width: 50,
  infrequency_items: [7],
  data: {survey: 'dass_d'},
  on_finish: function(data) {

    // Score response on infrequncy item.
    const scores = [1,1,0.5,0];
    data.infrequency = scores[data.responses['Q08']];

  }
}

// Behavioral Inhibition/Activation Scale (BIS/BAS)
var bisbas = {
  type: 'survey-template',
  items: [

    // Behavioral inhibition scale
    "I worry about making mistakes.",
    "Criticism or scolding hurts me quite a bit.",
    "I feel pretty worried or upset when I think or know somebody is angry at me.",
    "I feel worried when I think I have done poorly at something important.",

    // Behavioral activation scale (reward subscale)
    "When I get something I want, I feel excited and energized.",
    "When I'm doing well at something I love to keep at it.",
    "It would excite me to win a contest.",
    "When I see an opportunity for something I like I get excited right away.",

    // Behavioral activation scale (drive subscale)
    "When I want something I usually go all-out to get it.",
    "I go out of my way to get things I want.",
    "If I see a chance to get something I want I move on it right away.",
    "When I go after something I use a no-holds-barred approach.",

    // Infrequency item
    "I feel good when I am insulted by a good friend."

  ],
  scale: [
    "Very false<br>for me",               // scored as 0
    "Somewhat false<br>for me",           // scored as 1
    "Somewhat true<br>for me",            // scored as 2
    "Very true<br>for me"                 // scored as 3
  ],
  reverse: [
    false, false, false, false, false, false, false,
    false, false, false, false, false, false
  ],
  instructions: "For each item, indicate how much you agree or disagree with what the item says. Don't worry about being \"consistent\" in your responses.",
  scale_repeat: 7,
  survey_width: 1000,
  item_width: 40,
  infrequency_items: [12],
  data: {survey: 'bisbas'},
  on_finish: function(data) {

    // Score response on infrequncy item.
    const scores = [0,0.5,1,1];
    data.infrequency = scores[data.responses['Q13']];

  }
}

//------------------------------------//
// Define quality check
//------------------------------------//
// Check responses to infrequency items. Reject participants
// who respond carelessly on 2 or more items.

// Define infrequency item check.
var score_infrequency_items = function() {

  // Score infrequency items.
  const infreq = jsPsych.data.get().select('infrequency').sum();
  const sl = jsPsych.data.get().select('straightlining').sum();
  const zz = jsPsych.data.get().select('zigzagging').sum();
  return [infreq, sl, zz];

}

var infrequency_check = {
  type: 'call-function',
  func: score_infrequency_items,
  on_finish: function(trial) {
    if (jsPsych.data.getLastTrialData().values()[0].value[0] >= 2) {
      low_quality = true;
      jsPsych.endExperiment();
    }
  }
}

//------------------------------------//
// Define survey block
//------------------------------------//

// Define survey block
var SURVEYS = jsPsych.randomization.shuffle([gad7, dass, bisbas]);
SURVEYS.splice(0, 0, slider);
SURVEYS.push(infrequency_check);
