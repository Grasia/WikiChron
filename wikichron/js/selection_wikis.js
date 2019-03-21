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
function generate_badge({code, name, type}) {
    return `
        <div id="badge-${type}-${code}" class="badge badge-secondary p-2 current-selected-${type}" data-code="${code}">
            <span class="mr-2 align-middle">${name}</span>
            <button type="button" class="close close-wiki-badge align-middle" aria-label="Close" onclick="unselect_badge(this)">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `;
}

// create badge or remove it
function check_input({input, checked, type}) {
    var code = input.value;
    var name = input.dataset.name;
    var targetBadge;
    var newBadge;
    var badgesContainer;
    var is_wiki = type === 'wiki';

    if (checked) {
        newBadge = generate_badge({"code": code, "name": name, "type": type});

        if (is_wiki)
            badgesContainer = $('#wikis-badges-container');
        else
            badgesContainer = $('#metrics-badges-container');
        badgesContainer.append(newBadge);
    } else {
        targetBadge = document.getElementById(`badge-${type}-${code}`);
        targetBadge.remove();
    }

    check_enable_action_button();
}


// onclick for metrics checkboxes inputs
$('.metric-input').click(function(event) {
    var checked = $(this).is(':checked');
    check_input({"input": event.target, "checked": checked, "type": 'metric'});
});


// onclick for wikis checkboxes inputs
$('.wiki-input').click(function(event) {
    var checked = $(this).is(':checked');
    check_input({"input": event.target, "checked": checked, "type": 'wiki'});
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
$('#selection-footer-button').on ("click", function() {
    var selectedWikis = $('.current-selected-wiki');
    var selectedMetrics = $('.current-selected-metric');
    var target_app_url;
    var selection = '?';

    if (!selectedWikis || !selectedMetrics) { // In case user tries to bypass
                                            // the selection of the form inputs
        return;
    }

    for (let wiki of selectedWikis) {
        selection += `wikis=${wiki.dataset.code}&`
    }

    for (let metric of selectedMetrics) {
        selection += `metrics=${metric.dataset.code}&`
    }

    selection = selection.slice(0, -1);  // remove trailing '&'

    target_app_url = `/app/${selection}`

    window.location.href = encodeURI(target_app_url)

});
