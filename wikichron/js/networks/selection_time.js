var timeIndex;

$(function() {
    timeIndex = JSON.parse($('#time-axis-container').html());
})


function getDateFromSlider(sliderValue) {
    return timeIndex[sliderValue]
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

