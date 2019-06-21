/* List.js */
var wikisList;

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
        by = $( this ).data()['by']
        order = $( this ).data()['order']

        wikisList.sort(`wiki-${by}`, {
            order: order
        })
    })

}


updateHandleLabels = function(property, lower, upper, maxValue) {
    handle_lower = $( `#${property}-handle-lower` );
    handle_upper = $( `#${property}-handle-upper` );
    handle_lower.text( lower );
    if (upper == maxValue) {
        handle_upper.text( upper + '+');
    } else {
        handle_upper.text( upper );
    }
}



/* Filters */
const filter = {};

createFilterSlider = function(property, maxValue) {
    let handle_lower, handle_upper;

    let sliderVar = $( `#${property}-slider` ).slider({
        range: true,
        min: 0,
        max: maxValue, // zero-indexed
        values: [ 0, maxValue],
        step : maxValue / 200, // number of marks
        slide: function( event, ui ) {
            lower = ui.values[0];
            upper = ui.values[1];

            filter[`lower-${property}`] = lower;
            filter[`upper-${property}`] = upper;


            // Update display numbers
            updateHandleLabels(property, lower, upper, maxValue);

            const noUpperPages = filter['upper-pages'] == filter['max-pages'];
            const noUpperUsers = filter['upper-users'] == filter['max-users'];

            if (noUpperPages && filter['lower-pages'] == 0
             && noUpperUsers && filter['lower-users'] == 0) {
                wikisList.filter();
            } else {
                // Filter wikis by those numbers
                wikisList.filter(function(item) {

                    return (item.values()['wiki-pages'] >= filter['lower-pages']
                            && (noUpperPages ||
                                item.values()['wiki-pages'] <= filter['upper-pages'])
                            && item.values()['wiki-users'] >= filter['lower-users']
                            && (noUpperUsers
                                || item.values()['wiki-users'] <= filter['upper-users'])
                    );
                });
            }
        }
    });

    // Init display numbers with min and max values
    lower = sliderVar.slider( "values", 0 );
    upper = sliderVar.slider( "values", 1 );

    filter[`lower-${property}`] = lower;
    filter[`upper-${property}`] = upper;

    filter[`max-${property}`] = maxValue;

    updateHandleLabels(property, lower, upper, maxValue);

  }


// functions to run when DOM is ready
$(function()  {
    init_list_js();
    createFilterSlider('users', 20000);
    createFilterSlider('pages', 50000);
    setSortBy();
});

