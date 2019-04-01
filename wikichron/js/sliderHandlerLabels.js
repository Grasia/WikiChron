/**
 * This script is used to improve an dcc.RangeSlider
 * It adds an handler labels.
 * 
 * Copyright Youssef El Faqir El Rhazoui 
 */


// get the handlers
handlers = document.querySelectorAll("div.rc-slider-handle");
// get handlers date values
dates = document.querySelectorAll("#handler-labels");
for (i = 0; i < 2; i++){
    handlers[i].innerHTML += "<div class='handler-label'><p id=handler-label" + i + "></p></div>";
}

document.getElementById("handler-label-signal").addEventListener("DOMSubtreeModified", function(){
        val = document.getElementById("handler-label-signal").innerHTML.split("*")
        if (typeof val !== 'undefined' && val.length > 0) {
            document.getElementById('handler-label0').innerHTML = val[0]
            document.getElementById('handler-label1').innerHTML = val[1]
        }
    })