window.onload = function() {
  document.getElementById('fold-img-container').onclick = hideSideBar ;
}

function hideSideBar() {
  document.getElementById('side-bar').style({display: none});
}
