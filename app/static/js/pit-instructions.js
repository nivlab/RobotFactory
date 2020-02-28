//------------------------------------//
// Section 1: Prepare instructions
//------------------------------------//

var INSTRUCTIONS_01 = {
    type: 'pit-instructions',
    pages: [
      "../static/img/instructions01.png",
      "../static/img/instructions02.png",
      "../static/img/instructions03.png",
      "../static/img/instructions08.png",
      "../static/img/instructions05.png",
      "../static/img/instructions06.png",
      "../static/img/instructions07.png",
      "../static/img/instructions08.png",
    ],
    show_clickable_nav: true,
    button_label_previous: "Prev",
    button_label_next: "Next"
}


var PRACTICE_GO = [
  {'Trial':  1, 'Valence': 'Win',  'Action': 'Go', 'Correct': 32},
  {'Trial':  2, 'Valence': 'Win',  'Action': 'Go', 'Correct': 32},
  {'Trial':  3, 'Valence': 'Win',  'Action': 'Go', 'Correct': 32},
  {'Trial':  4, 'Valence': 'Win',  'Action': 'Go', 'Correct': 32},
];


var PRACTICE_NO_GO = [
  {'Trial':  1, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1},
  {'Trial':  2, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1},
  {'Trial':  3, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1},
  {'Trial':  4, 'Valence': 'Lose', 'Action': 'No-Go', 'Correct': -1},
];
