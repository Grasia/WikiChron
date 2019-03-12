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

function init_current_selection() {

    /* init wikis current selection */
    var checkedBoxes = $('.wiki-checkbox').
                        filter( function(index, element){
                            return element.checked
                        })
    if (checkedBoxes.length > 0) {
        var badgesContainer = $('#wiki-badges-container');
        var wikiCode = checkedBoxes[0].value;
        var wikiName = checkedBoxes[0].dataset.wikiName;
        var badgeSelectedWiki = `
        <span id="current-selected-wiki" class="badge badge-secondary p-2 align-middle" data-code="${wikiCode}">
            ${wikiName}
        </span>`
        badgesContainer.html(badgeSelectedWiki);

        //~ $('#selection-footer-button')[0].disabled = false;
    } else {
        //~ $('#selection-footer-button')[0].disabled = true;
    }

    /* init networks current selection */
    var radioButtons = $('.networks-radiobutton').
                        filter( function(index, element){
                            return element.checked
                        })
    if (radioButtons.length > 0) {
        badgesContainer = $('#network-badges-container');
        var networkCode = radioButtons[0].value;
        var networkName = radioButtons[0].dataset.networkName;
        var badgeSelectedNetwork = `
            <span id="current-selected-network" class="badge badge-secondary p-2 align-middle" data-network-code="${networkCode}">
                ${networkName}
            </span>
        `
        badgesContainer.html(badgeSelectedNetwork);
    }
}

init_current_selection()


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
