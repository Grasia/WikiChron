/**
 * This script is used to improve an dcc.RangeSlider
 * It adds an handler labels.
 * 
 * Copyright Youssef El Faqir El Rhazoui 
 */

const MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
var time_index = document.querySelector("#dates-index").innerHTML;
time_index = time_index.replace(/[\\"]/g, "");
time_index = time_index.split(", ");

function update_labels(mutation) {
    let val = parseInt(mutation.target.getAttribute("aria-valuenow"), 10);

    time = time_index[val];
    time = time.split("-");
    month = MONTH[parseInt(time[1])-1]
    date = `${month} ${time[0]}`
    mutation.target.children[0].children[0].innerHTML = date
}


// get the handlers
handlers = document.querySelectorAll("div.rc-slider-handle");
// get handlers date values
dates = document.querySelectorAll("#handler-labels");
handlerClasses = ['handler-label-left', 'handler-label-right']

for (i = 0; i < handlerClasses.length; i++){
    handlers[i].innerHTML += `<div class='handler-label ${handlerClasses[i]}'><p id=handler-label${i}></p></div>`;

    // now, add event when value change
    observer = new MutationObserver( function(mutations){
        mutations.forEach(update_labels);
    });
    observer.observe(handlers[i], { attributes: true});
}