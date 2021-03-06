'use strict';


/* enable action button */
function check_enable_action_button() {
    var selectedWikisNo = $('#wiki-badges-container')[0].children.length
    var selectedNetworksNo = $('#network-badges-container')[0].children.length

    if (selectedWikisNo > 0) { // enable Time selection tab
        $('#time-tab').removeClass('disabled');
    } else {
        $('#time-tab').addClass('disabled');
    }

    if (selectedWikisNo > 0 && selectedNetworksNo > 0) {
        $('#selection-footer-button')[0].disabled = false;
    } else {
        $('#selection-footer-button')[0].disabled = true;
    }
};


/* checkboxes logic */


// aux function
function generate_wiki_badge(wikiCode, wikiName) {
    return `
        <div id="current-selected-${wikiCode}" class="badge badge-secondary current-selected-wiki align-middle" data-code="${wikiCode}">
            <span>${wikiName}</span>
        </div>
    `;
}


// aux function
function generate_network_badge(networkCode, networkName) {
    return `
        <div id="" class="badge badge-secondary align-middle current-selected-network" data-code="${networkCode}">
            <span>${networkName}</span>
        </div>
    `;
}


// onclick for network radiobuttons inputs
$('.networks-radiobutton').on( "click", function({target}) {
    var networkCode = target.value;
    var networkName = target.dataset.networkName;
    var badgeSelectedNetwork = generate_network_badge(networkCode, networkName);
    var badgesContainer = $('#network-badges-container');
    badgesContainer.html(badgeSelectedNetwork);

    check_enable_action_button();

});


// onclick for wikis checkboxes input
$('.wiki-input').on( "click", function({target}) {
    var wikiCode = target.value;
    var badgesContainer = $('#wiki-badges-container');
    var sameWiki = false;

    if (badgesContainer[0].children.length) { // If there is already a selection
        var currentBadge = badgesContainer[0].children[0];
        var currentWikiCode = currentBadge.dataset.code;
        sameWiki = currentWikiCode === target.value;
        if (sameWiki) { // if same as previous selected, clean current selection
           badgesContainer.html('');
        } else { // if different, unselect previous wiki
            // Clear search in order to uncheck a wiki card
            // Because of https://github.com/javve/list.js/issues/380
            wikisList.search('')
            document.getElementById('search-wiki-input').value = "";

            $(`input[id="checkbox-${currentWikiCode}"]`)[0].checked = false;
        }
    }

    if (!sameWiki) {
        // Add badge of last selected wiki
        var wikiName = target.dataset.name;
        var badgeSelectedWiki = generate_wiki_badge(wikiCode, wikiName);

        badgesContainer.html(badgeSelectedWiki);
    }

    check_enable_action_button();

});


function init_current_selection() {

    /* init wikis current selection */
    var checkedBoxes = $('.wiki-input').
                        filter( function(index, element){
                            return element.checked
                        })
    if (checkedBoxes.length > 0) {
        var badgesContainer = $('#wiki-badges-container');
        var wikiCode = checkedBoxes[0].value;
        var wikiName = checkedBoxes[0].dataset.name;
        var badgeSelectedWiki = generate_wiki_badge(wikiCode, wikiName);
        badgesContainer.html(badgeSelectedWiki);
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
        var badgeSelectedNetwork = generate_network_badge(networkCode, networkName);
        badgesContainer.html(badgeSelectedNetwork);
    }

    check_enable_action_button();
}


function getDateFromSlider(sliderValue) {
    return dateIndex[sliderValue]
}


/* press action button */
$('#selection-footer-button').on ("click", function() {
    var selectedWiki = $('.current-selected-wiki')[0];
    var selectedNetwork = $('.current-selected-network')[0];
    var target_app_url;
    var selection;
    var timeSelection;
    var lowerBound, upperBound;

    if (!selectedWiki || !selectedNetwork) { // In case user tries to bypass
                                            // the selection of the form inputs
        return;
    }

    timeSelection =  $('#time-slider').slider("option", "values")
    lowerBound = getDateFromSlider(timeSelection[0]) / 1000;
    upperBound = getDateFromSlider(timeSelection[1]) / 1000;

    selection = `?wikis=${selectedWiki.dataset.code}&network=${selectedNetwork.dataset.code}&lower_bound=${lowerBound}&upper_bound=${upperBound}`

    target_app_url = `/networks/app/${selection}`

    window.location.href = encodeURI(target_app_url)

});


// functions to run when DOM is ready
$(function()  {
    init_current_selection();
});
