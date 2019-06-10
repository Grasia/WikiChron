/**
 * This script is used to add a hint in filter table
 *
 * Copyright Youssef El Faqir El Rhazoui
 */

var hints = ["e.g: eq \"name\"", "e.g: > \"50\""];
var headers = document.getElementById("ranking-table").getElementsByClassName("dash-filter");

headers[0].innerHTML += `<div class='hint non-show'><p>${hints[0]}</p></div>`;
headers[0].firstChild.addEventListener("focus", function(){
    headers[0].children[1].style.display = 'initial';
});
headers[0].firstChild.addEventListener("blur", function(){
    headers[0].children[1].style.display = 'none';
});

headers[1].innerHTML += `<div class='hint hint-2 non-show'><p>${hints[1]}</p></div>`;
headers[1].firstChild.addEventListener("focus", function(){
    headers[1].children[1].style.display = 'initial';
});
headers[1].firstChild.addEventListener("blur", function(){
    headers[1].children[1].style.display = 'none';
});