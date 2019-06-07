var wikisList;

/* List.js */
init_list_js = function() {
    var options = {
        valueNames: [ 'wiki-name', 'wiki-url',  'wiki-lastUpdated', 'wiki-users',
                    'wiki-edits']
    };

    wikisList = new List('wiki-cards-container', options);

    onlySearch = ['wiki-name', 'wiki-url']

    $('#search-wiki-input').on('keyup', function() {
        let searchString = $(this).val();
        wikisList.search(searchString, onlySearch);
    });

    // Start list sorted by last update value
    wikisList.sort('wiki-lastUpdated', {
        order: 'desc'
    })
}


/* Sort By */
setSortBy = function() {

    $('.dropdown-item').on('click', function () {
        console.log( $( this ).data()['order'] )
        by = $( this ).data()['by']
        order = $( this ).data()['order']

        wikisList.sort(`wiki-${by}`, {
            order: order
        })


    })

}



/* Filters */
createUsersSlider = function() {
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


// functions to run when DOM is ready
$(function()  {
    init_list_js();
    //~ createUsersSlider();
    setSortBy();
});

