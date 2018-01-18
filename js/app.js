document.addEventListener("DOMContentLoaded", setEvents);

function setEvents() {
    console.log('Hello');
    document.getElementById('fold-img-container').onclick = hideSideBar;
}

function hideSideBar() {
  document.getElementById('side-bar').style.display = 'none';
}
