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
$('.wiki-checkbox').on( "click", enable_action_button)

var chosenWiki;
function enable_action_button() {
    var checkedBoxes = $('.wiki-checkbox').
                        filter( function(index, element){
                            return element.checked
                        })
    if (checkedBoxes.length === 1) {
        chosenWiki = checkedBoxes[0].value;
        $('#selection-footer-button')[0].disabled = false;
    } else {
        $('#selection-footer-button')[0].disabled = true;
    }
};

// init action button enable/disable
enable_action_button()

/* press action button */
$('#selection-footer-button').on ("click", function() {
    var chosenNetwork = $('.networks-radiobutton').
                        filter( function(index, element){
                            return element.checked
                        })[0].value
    console.log(chosenNetwork);
    console.log(chosenWiki);

    if (!chosenNetwork || !chosenWiki) { // In case user tries to bypass
                                         // the selection of the form inputs
        return
    }

    window.location.href = "/app/?" + "wikis=" + chosenWiki + "&network=" + chosenNetwork

});
