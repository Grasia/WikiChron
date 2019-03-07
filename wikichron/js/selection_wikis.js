'use strict';

/* List.js */
var options = {
    valueNames: [ 'wiki-name', 'wiki-url' ]
};

var wikisList = new List('cards-container', options);

$('#search-wiki-input').on('keyup', function() {
    var searchString = $(this).val();
    wikisList.search(searchString);
});

/* enable action button */
$('.wiki-checkbox').on( "click", function() {
    var checkedBoxes = $('.wiki-checkbox').
                        filter( function(index, element){
                            return element.checked
                        })
    if (checkedBoxes.length === 1) {
        enable_action_button();
    } else {
        disable_action_button();
    }
});

function enable_action_button() {
    $('#selection-footer-button')[0].disabled = false;
}

function disable_action_button() {
    $('#selection-footer-button')[0].disabled = true;
}

/* press action button */
//~ $('#selection-footer-button').on ("click", function() {
    //~ var chosenWiki = $('.wiki-checkbox').
                        //~ filter( function(index, element){
                            //~ return element.checked
                        //~ })[0].value
    //~ console.log(chosenWiki);

    //~ var chosenNetwork = $('.networks-radiobutton').
                        //~ filter( function(index, element){
                            //~ return element.checked
                        //~ })[0].value
    //~ console.log(chosenNetwork);

    //~ $('#selection-footer-button')[0].formaction = "wikis=" + chosenWiki + "&networks=" + chosenNetwork

//~ });
