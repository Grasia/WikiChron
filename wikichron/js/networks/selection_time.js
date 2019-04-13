var dateIndex = [];

$(function() {
    var wikiCode = 'cocktails.fandom.com'
    //~ var dateFirst = new Date($('#time-axis-first').html());
    //~ var dateLast = new Date($('#time-axis-last').html());
    var times = JSON.parse($('#time-spans-container').html());
    var dateFirst = new Date(times[wikiCode]['first_date']);
    var dateLast = new Date(times[wikiCode]['last_date']);
    console.log(dateFirst);
    console.log(dateLast);
    var d = dateFirst;
    while (d < dateLast) {
        //~ dateIndex.push(`${d.getMonth()} ${d.getUTCFullYear()}`);
        dateIndex.push(d.toLocaleString('en-US', { timeZone: 'UTC', formatMatcher: 'basic', month: 'short', year: "numeric" }))
        d.setMonth(d.getMonth() + 1);
    }

    dateIndex.push(dateLast.toLocaleString('en-US', { timeZone: 'UTC', formatMatcher: 'basic', month: 'short', year: "numeric" }))
})


function getDateFromSlider(sliderValue) {
    return dateIndex[sliderValue]
}


$( function() {
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

  } );

