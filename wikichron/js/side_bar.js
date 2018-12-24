function setEvents() {
    console.log('Setting js events for side_bar.py...');
    document.getElementById('fold-img-container').onclick = hideSideBar;
    console.log('All Set!');
}

function hideSideBar() {

    console.log('Pressed hide side bar...');
    // makes arrows point to the right >>
    fold_button = document.getElementById('fold-button');
    fold_button.style.transform = "rotateY(180deg)";


    // effect pushing away side_bar (transform: translate - X)

    // hide side bar
    document.getElementById('side-bar-content').style.display = 'none';
    document.getElementById('side-bar-root').style.flex = 'unset';

    // set show bar in arrow
    fold_container = document.getElementById('fold-img-container');
    fold_container.onclick = showSideBar;
    fold_container.style.margin = '5px 5px 0px 5px';
}

function showSideBar() {

    console.log('Pressed show side bar...');

    // makes arrows point to the left <<
    fold_button = document.getElementById('fold-button');
    fold_button.style.transform = '';

    // effect pushing away side_bar (transform: translate - X)

    // show side bar
    document.getElementById('side-bar-content').style.display = '';
    document.getElementById('side-bar-root').style.flex = '';

    // set hide bar in arrow
    fold_container = document.getElementById('fold-img-container');
    fold_container.onclick = hideSideBar;
    fold_container.style.margin = '';
}


setEvents()
