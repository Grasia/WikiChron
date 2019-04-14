var dateIndex;
var wikisTimelifes;

function getSelectedWikiCode (){
    var selectedWiki = $('.current-selected-wiki')[0]
    if (selectedWiki) {
        return selectedWiki.dataset.code;
    } else {
        return false
    }
}

onChangeWiki = function() {
    var wikiCode = getSelectedWikiCode();

    if (!wikiCode) return;

    dateIndex = []
    var dateFirst = new Date(wikisTimelifes[wikiCode]['first_date']);
    var dateLast = new Date(wikisTimelifes[wikiCode]['last_date']);
    var d = dateFirst;
    while (d < dateLast) {
        //~ dateIndex.push(`${d.getMonth()} ${d.getUTCFullYear()}`);
        dateIndex.push(d.toLocaleString('en-US', { timeZone: 'UTC', formatMatcher: 'basic', month: 'short', year: "numeric" }))
        d.setMonth(d.getMonth() + 1);
    }

    dateIndex.push(dateLast.toLocaleString('en-US', { timeZone: 'UTC', formatMatcher: 'basic', month: 'short', year: "numeric" }))

    createSlider();
}


function getDateFromSlider(sliderValue) {
    return dateIndex[sliderValue]
}


createSlider = function() {
    var lower;
    var upper;

    monthsNo = dateIndex.length
    months10Percentage = Math.round(monthsNo * 0.1)

    $( "#slider-range" ).slider({
        range: true,
        min: 0,
        max: monthsNo - 1, // zero-indexed
        values: [ 0, months10Percentage],
        step : 1,
        slide: function( event, ui ) {
            lower = ui.values[ 0 ]
            upper = ui.values[ 1 ]
            $( "#time-axis-selection" ).html(getDateFromSlider(lower) + " - " + getDateFromSlider(upper));
      }
    });

    // Init display numbers
    lower = $( "#slider-range" ).slider( "values", 0 )
    upper = $( "#slider-range" ).slider( "values", 1 )
    $( "#time-axis-selection" ).html(
        getDateFromSlider(lower) +
        " - " +
        getDateFromSlider(upper)
    )

  }


$( function () { // on load

    // Request time lifes for all wikis
    var request = $.ajax({
            url: "/wikisTimelifes.json",
            method: "GET",
            dataType: "json",
            async: false
        });

    request.done(function( data ) {
        wikisTimelifes = data;
    });

    request.fail(function( jqXHR, textStatus ) {
        alert( "Request failed: " + textStatus + ".\n Please, reload the browser.");
    });

    // bind onChangeWiki when the wiki badge changes
    $('#wiki-badges-container').bind("DOMSubtreeModified", function() {
        onChangeWiki();
    });
});
