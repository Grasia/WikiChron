function setEvents() {
    console.log('Setting js events for main/share_modal...');
    var modal_buttons = document.getElementsByClassName ('share-modal-button-cn')

    for (let button of modal_buttons) {
      //~ console.log(button);
      button.onclick = () => actionCopy(button.id);
      button.onmouseleave = () => switchTooltipToCopy(button.id);
      button.appendChild(createTooltipElement(button.id))
    }

    console.log('All Set!');
}

function actionCopy(input_id) {

  ta_id = input_id + '-input'
  /* Get the text field */
  var copyText = document.getElementById(ta_id);

  /* Select the text field */
  copyText.select();

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  var tooltip = document.getElementById(input_id + '-tooltiptext');
  tooltip.innerHTML = "Copied!";

}

function createTooltipElement(input_id) {
  txt = document.createTextNode('Copy to clipboard')
  span = document.createElement('span');
  span.appendChild(txt);
  span.className = 'tooltiptext';
  span.id = input_id + '-tooltiptext';
  //~ console.log(span);
  return span;
}

function switchTooltipToCopy(input_id) {
  tooltiptext = document.getElementById(input_id + '-tooltiptext');
  tooltiptext.innerText = 'Copy to clipboard';
}

setEvents()
//~ setTimeout(function(){ setEvents() }, 1000);
