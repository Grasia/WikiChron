var wikisList;

/* List.js */
function init_list_js() {
    var options = {
        valueNames: [ 'wiki-name', 'wiki-url',  ]
    };

    wikisList = new List('wiki-cards-container', options);

    onlySearch = ['wiki-name', 'wiki-url']

    $('#search-wiki-input').on('keyup', function() {
        let searchString = $(this).val();
        wikisList.search(searchString, onlySearch);
    });

}

// functions to run when DOM is ready
$(function()  {
    init_list_js();
});

