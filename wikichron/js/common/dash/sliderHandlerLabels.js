/**
 * This script is used to improve an dcc.RangeSlider
 * It adds an handler labels.
 *
 * Copyright 2019 Youssef El Faqir El Rhazoui
 * Copyright 2019 Abel Serrano Juste
 */

const MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
// get the handlers
const handlers = document.querySelectorAll("div.rc-slider-handle");
// get handlers date values
const dates = document.querySelectorAll("#handler-labels");
const handlerClasses = ['handler-label-left', 'handler-label-right']


function get_date(val) {
    let time_index = document.querySelector(".time-index").innerHTML;
    // In networks we don't have "relative dates", so here we check if we have that checklist option
    const variableTimeAxis = document.querySelector("#time-axis-selection");
    // Very hacky way to obtain know if we are in relative or absolute dates (for WCh "classic")
    const relativeDates = variableTimeAxis && document.querySelector("#time-axis-selection > label:nth-child(1) > input").checked;

    if (relativeDates) {
        time_index = JSON.parse(time_index);
        date = time_index[val];
    } else {
        // Get list of all day and month in "words" for this wiki selection
        time_index = time_index.replace(/\"/g, "").slice(1,-1);
        time_index = time_index.split(", ");
        // Get actual value we want to display
        time = time_index[val];
        time = time.split("-");
        month = MONTH[parseInt(time[1])-1]
        date = `${month} ${time[0]}`
    }

    return date;
}


function update_labels(mutation) {

    if (mutation['attributeName'] === "aria-valuenow") {
        const val = parseInt(mutation.target.getAttribute("aria-valuenow"), 10);
        mutation.target.children[0].children[0].innerHTML = get_date(val);
    }
}


function init_labels(handler, handlerId) {
    const val = parseInt(handler.getAttribute("aria-valuenow"), 10);
    document.getElementById(handlerId).innerHTML = get_date(val);
}


/* Setting slider handle observers*/
let observer;
for (i = 0; i < handlerClasses.length; i++){
    handlers[i].innerHTML += `<div class='handler-label ${handlerClasses[i]}'><p id=handler-label${i}></p></div>`;

    // now, add event when value change
    observer = new MutationObserver( function(mutations){
        mutations.forEach(update_labels);
    });
    observer.observe(handlers[i], { attributes: true});
}


/* Setting time index observer */
const timeIndexDiv = document.querySelector(".time-index");
const ready = document.querySelector("#ready");
const initHandlerLabelsObserver = new MutationObserver(function(mutations, observer) {

    mutations.forEach(function(){

        for (i = 0; i < handlerClasses.length; i++){
            init_labels(handlers[i], `handler-label${i}`);
        }
    });
});

initHandlerLabelsObserver.observe(ready, {childList: true}); // initialization
initHandlerLabelsObserver.observe(timeIndexDiv, {subtree: true, characterData: true}); // when timeIndex changes




