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
function check_enable_action_button() {
    var selectedWikisNo = $('#wikis-badges-container')[0].children.length
    var selectedMetricsNo = $('#metrics-badges-container')[0].children.length
    if (selectedWikisNo > 0 && selectedMetricsNo > 0) {
        $('#selection-footer-button')[0].disabled = false;
    } else {
        $('#selection-footer-button')[0].disabled = true;
    }
};


/* checkboxes logic */

// to bind to onclick of unselect_badge
function unselect_badge(target) {
    var target_badge = target.parentNode;
    var code = target_badge.dataset.code;
    $(`input[id="checkbox-${code}"]`)[0].checked = false;
    target_badge.remove();
    check_enable_action_button();
}


// aux function
function generate_badge({code, name}) {
    return `
        <div id="current-selected-${code}" class="badge badge-secondary p-2 current-selected" data-code="${code}">
            <span class="mr-2 align-middle">${name}</span>
            <button type="button" class="close close-wiki-badge align-middle" aria-label="Close" onclick="unselect_badge(this)">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `;
}


// onclick for metrics checkboxes inputs
$('.metric-checkbox').click(function(event) {
    console.log(event);
    var metricCode = event.target.value;
    var metricName = event.target.dataset.metricName;
    var checked = $(this).is(':checked')

    if (checked) {
        var badgeSelectedMetric = generate_badge({"code": metricCode, "name": metricName});
        var badgesContainer = $('#metrics-badges-container');
        badgesContainer.append(badgeSelectedMetric);
    } else {
        var target_badge = $(`#current-selected-${metricCode}`)[0];
        target_badge.remove();
    }

    check_enable_action_button();

});


// onclick for wikis checkboxes input
$('.wiki-checkbox').on( "click", function({target}) { //TOMERGE with previous one
    var wikiCode = target.value;
    var badgesContainer = $('#wikis-badges-container');
    var sameWiki = false;

    if (badgesContainer[0].children.length) { // If there is already a selection
        var currentBadge = badgesContainer[0].children[0];
        var currentWikiCode = currentBadge.dataset.code;
        sameWiki = currentWikiCode === target.value;
        if (sameWiki) { // if same as previous selected, clean current selection
           badgesContainer.html('');
        } else { // if different, unselect previous wiki
            $(`input[id="checkbox-${currentWikiCode}"]`)[0].checked = false;
        }
    }

    if (!sameWiki) {
        // Add badge of last selected wiki
        var wikiName = target.dataset.wikiName;
        var badgeSelectedWiki = generate_badge({"code": wikiCode, "name": wikiName});

        badgesContainer.html(badgeSelectedWiki);
    }

    check_enable_action_button();

});


function init_current_selection() {

    /* init wikis current selection */
    var checkedBoxes = $('.wiki-checkbox').
                        filter( function(index, element){
                            return element.checked
                        })
    if (checkedBoxes.length > 0) {
        var badgesContainer = $('#wikis-badges-container');
        var wikiCode = checkedBoxes[0].value;
        var wikiName = checkedBoxes[0].dataset.wikiName;
        var badgeSelectedWiki = generate_wiki_badge(wikiCode, wikiName);
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
        var badgeSelectedNetwork = generate_network_badge(networkCode, networkName);
        badgesContainer.html(badgeSelectedNetwork);
    }

    check_enable_action_button();
}


init_current_selection()


/* press action button */
$('#selection-footer-button').on ("click", function() { //TOFIX
    var selectedWiki = $('.current-selected-wiki')[0];
    var selectedNetwork = $('.current-selected-metric')[0];
    var target_app_url;

    if (!selectedWiki || !selectedNetwork) { // In case user tries to bypass
                                            // the selection of the form inputs
        return
    }

    target_app_url = `/app/?wikis=${selectedWiki.dataset.code}&metrics=${selectedNetwork.dataset.code}`

    window.location.href = encodeURI(target_app_url)

});
