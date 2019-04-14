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
    var firstMonth = new Date(dateFirst.getFullYear(), dateFirst.getMonth(), 1, 0, 0, 0)
    var lastMonth = new Date(dateLast.getFullYear(), dateLast.getMonth(), 1, 0, 0, 0)
    var d = firstMonth;
    console.log(d.getTime());
    while (d <= lastMonth) {
        dateIndex.push(d.getTime())
        d.setMonth(d.getMonth() + 1);
    }

    dateIndex.push(lastMonth)

    createSlider();
}


function getDateFromSlider(sliderValue) {
    return dateIndex[sliderValue]
}


function formatDate (unixDate) {
    date = new Date(unixDate)
    return date.toLocaleString('en-US',
                                { formatMatcher: 'basic',
                                  month: 'short', year: "numeric" })
}


createSlider = function() {
    var lower;
    var upper;

    monthsNo = dateIndex.length
    months10Percentage = Math.round(monthsNo * 0.1)

    $( "#time-slider" ).slider({
        range: true,
        min: 0,
        max: monthsNo - 1, // zero-indexed
        values: [ 0, months10Percentage],
        step : 1,
        slide: function( event, ui ) {
            lower = ui.values[ 0 ]
            upper = ui.values[ 1 ]
            $( "#time-axis-selection" ).html(formatDate(getDateFromSlider(lower)) + " - " + formatDate(getDateFromSlider(upper)));
      }
    });

    // Init display numbers
    lower = $( "#time-slider" ).slider( "values", 0 )
    upper = $( "#time-slider" ).slider( "values", 1 )
    $( "#time-axis-selection" ).html(
        formatDate(getDateFromSlider(lower)) +
        " - " +
        formatDate(getDateFromSlider(upper))
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
        console.log( "Request for wikisTimelifes.json failed: " + textStatus + ".\n Please, try reloading the browser or contacting us.");
    });

    // bind onChangeWiki when the wiki badge changes
    $('#wiki-badges-container').bind("DOMSubtreeModified", function() {
        onChangeWiki();
    });

    onChangeWiki(); // call on initial load
});
