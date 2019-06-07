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
    var handle_lower, handle_upper;

    maxUsers = 1000;

    $( "#users-slider" ).slider({
        range: true,
        min: 0,
        max: maxUsers, // zero-indexed
        values: [ 0, maxUsers],
        step : 100,
        slide: function( event, ui ) {
            lower = ui.values[ 0 ]
            upper = ui.values[ 1 ]

            // Update display numbers
            handle_lower = $( "#users-handle-lower" );
            handle_upper = $( "#users-handle-upper" );
            console.log(lower, upper);
            handle_lower.text( lower );
            handle_upper.text( upper );

            // Filter wikis by this numbers
            wikisList.filter(function(item) {
                console.log(item.values()['wiki-users']);
                if (item.values()['wiki-users'] >= lower
                    && item.values()['wiki-users'] <= upper) {
                   return true;
                } else {
                   return false;
                }
            });
        }
    });

    // Init display numbers
    lower = $( "#users-slider" ).slider( "values", 0 )
    upper = $( "#users-slider" ).slider( "values", 1 )

    handle_lower = $( "#users-handle-lower" );
    handle_upper = $( "#users-handle-upper" );

    handle_lower.text( lower );
    handle_upper.text( upper );

  }


// functions to run when DOM is ready
$(function()  {
    init_list_js();
    createUsersSlider();
    setSortBy();
});

