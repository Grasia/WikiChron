'use strict';


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

    return false; // Prevents any other event that could trigger in any ancestor element, like an anchor href, to trigger.

}


// aux function
function generate_badge({code, name, type}) {
    if (type === 'metric') {
        return `
            <div id="badge-${type}-${code}" class="badge badge-secondary current-selected-${type}" data-code="${code}">
                <span class="mr-2 align-middle">${name}</span>
                <button type="button" class="close close-wiki-badge align-middle" aria-label="Close" onclick="return unselect_badge(this)">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `;
    } else {
        return `
            <div id="badge-${type}-${code}" class="badge badge-secondary current-selected-${type}" data-code="${code}">
                <span class="mr-2 align-middle">${name}</span>
            </div>
        `;
    }
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
    var input = event.target
    var code = input.value;
    var name = input.dataset.name;
    var targetBadge;
    var newBadge;
    var badgesContainer;
    var type = 'metric';

    if (checked) {
        newBadge = generate_badge({"code": code, "name": name, "type": type});
        badgesContainer = $('#metrics-badges-container');
        badgesContainer.append(newBadge);
    } else {
        targetBadge = document.getElementById(`badge-${type}-${code}`);
        targetBadge.remove();
    }

    check_enable_action_button();
});


// onclick for wikis checkboxes input
$('.wiki-input').on( "click", function({target}) {
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
        var badgeSelectedWiki = generate_badge({"code": wikiCode,
                                                "name": wikiName,
                                                "type": "wiki"});

        badgesContainer.html(badgeSelectedWiki);
    }

    check_enable_action_button();

});


function create_badges_in_container(inputs, container, type) {
    for (let input of inputs) {
        let code = input.value;
        let name = input.dataset.name;
        var newBadge = generate_badge({code, name, type});
        container.append(newBadge);
    }

}


function unfoldCategoryMetrics(catName) {
    document.getElementById(catName).classList.add('show');
}


function init_current_selection() {
    var checkedBoxes;
    var badgesContainer;

    /* init wikis current selection */
    checkedBoxes = $('.wiki-input').
                        filter( function(index, element){
                            return element.checked
                        })
    badgesContainer = $('#wikis-badges-container');
    create_badges_in_container(checkedBoxes, badgesContainer, 'wiki');


    /* init metrics current selection */
    checkedBoxes = $('.metric-input').
                        filter( function(index, element){
                            return element.checked
                        })

    badgesContainer = $('#metrics-badges-container');
    create_badges_in_container(checkedBoxes, badgesContainer, 'metric');
    for (let metric of checkedBoxes) {
        unfoldCategoryMetrics(metric.dataset.catName);
    }

    check_enable_action_button();

}


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

    target_app_url = `/monowiki/app/${selection}`

    window.location.href = encodeURI(target_app_url)

});


// functions to run when DOM is ready
$(function()  {
    init_list_js();
    init_current_selection();
});
