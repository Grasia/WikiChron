var dateIndex = [];

$(function() {
    var dateFirst = new Date($('#time-axis-first').html());
    var dateLast = new Date($('#time-axis-last').html());
    console.log(dateFirst);
    console.log(dateLast);
    var d = dateFirst;
    while (d < dateLast) {
        //~ dateIndex.push(`${d.getMonth()} ${d.getUTCFullYear()}`);
        dateIndex.push(d.toLocaleString('en-US', { timeZone: 'UTC', formatMatcher: 'basic', month: 'short', year: "numeric" }))
        d.setMonth(d.getMonth() + 1);
    }
})


function getDateFromSlider(sliderValue) {
    return dateIndex[sliderValue]
}


$( function() {
    var lower;
    var upper;

    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 500,
      values: [ 0, 1 ],
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

