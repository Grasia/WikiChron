/**
 * This script is used to improve an dcc.RangeSlider
 * It adds an handler labels.
 * 
 * Copyright Youssef El Faqir El Rhazoui 
 */

 const TIME_DIV = 60 * 60 * 24 * 30;
 const MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

function update_labels(mutation) {
    let val = parseInt(mutation.target.getAttribute("aria-valuenow"), 10);
    let time = parseInt(document.querySelector("#first-entry-signal").innerHTML, 10);
    val = time + val * TIME_DIV;
    let date = new Date(0);
    date.setUTCSeconds(val);
    date = MONTH[date.getMonth()] + " " + date.getFullYear();
    mutation.target.children[0].children[0].innerHTML = date
}


// get the handlers
handlers = document.querySelectorAll("div.rc-slider-handle");
// get handlers date values
dates = document.querySelectorAll("#handler-labels");

for (i = 0; i < 2; i++){
    handlers[i].innerHTML += "<div class='handler-label'><p id=handler-label" + i + "></p></div>";

    // now, add event when value change
    observer = new MutationObserver( function(mutations){
        mutations.forEach(update_labels);
    });
    observer.observe(handlers[i], { attributes: true});
}