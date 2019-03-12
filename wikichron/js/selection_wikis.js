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

/* checkboxes logic */
$('.wiki-checkbox').on( "click", function({target}) {
    var wikiCode = target.value;
    var badgesContainer = $('#wiki-badges-container');
    if (badgesContainer[0].children.length) { // If there is already a selection
        var currentBadge = badgesContainer[0].children[0];
        var currentWikiCode = currentBadge.dataset.code;
        if (currentWikiCode === target.value) { // if same as previous selected, clean and finish
           badgesContainer.html('');
           return;
        } else { // if different, unselect previous wiki
            $(`input[id="checkbox-${currentWikiCode}"]`)[0].checked = false;
        }
    }

    // Add badge of last selected wiki
    var wikiName = target.dataset.wikiName;
    var badgeSelectedWiki = `<span id="current-selected-wiki" class="badge badge-secondary p-2 align-middle" data-code="${wikiCode}">${wikiName}</span>`
    badgesContainer.html(badgeSelectedWiki);

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

    window.location.href = `/app/?wikis=${chosenWiki}&network=${chosenNetwork}`

});
