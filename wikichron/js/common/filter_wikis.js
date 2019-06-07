var wikisList;

/* List.js */
init_list_js = function() {
    var options = {
        valueNames: [ 'wiki-name', 'wiki-url',  'wiki-lastUpdated', 'wiki-users',
                    'wiki-edits', 'wiki-pages']
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
createSlider = function(property, maxValue) {
    var lower;
    var upper;
    var handle_lower, handle_upper;

    let sliderVar = $( `#${property}-slider` ).slider({
        range: true,
        min: 0,
        max: maxValue, // zero-indexed
        values: [ 0, maxValue],
        step : 100, // number of marks
        slide: function( event, ui ) {
            lower = ui.values[ 0 ]
            upper = ui.values[ 1 ]

            // Update display numbers
            handle_lower = $( `#${property}-handle-lower` );
            handle_upper = $( `#${property}-handle-upper` );
            handle_lower.text( lower );
            handle_upper.text( upper );

            // Filter wikis by those numbers
            wikisList.filter(function(item) {
                if (item.values()[`wiki-${property}`] >= lower
                    && item.values()[`wiki-${property}`] <= upper) {
                   return true;
                } else {
                   return false;
                }
            });
        }
    });

    // Init display numbers with min and max values
    lower = sliderVar.slider( "values", 0 )
    upper = sliderVar.slider( "values", 1 )

    handle_lower = $( `#${property}-handle-lower` );
    handle_upper = $( `#${property}-handle-upper` );
    handle_lower.text( lower );
    handle_upper.text( upper );

  }


// functions to run when DOM is ready
$(function()  {
    init_list_js();
    createSlider('users', 20000);
    createSlider('pages', 20000);
    setSortBy();
});

