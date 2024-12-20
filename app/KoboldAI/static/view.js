// Get the modal
var debugnav = document.getElementById("navbar");

// Get the button that opens the modal
var btn = document.getElementById("debugbutton");

// State of Visibility
var debugstate = false;

// When the user clicks on the button, open the modal
btn.onclick = function () {
  console.log(get_demo_player())
  if (debugstate == false) {
    debugnav.style.visibility  = "hidden"
    //console.log('Hidden!')
    debugstate = true
  }else{
    debugnav.style.visibility  = "visible"
    //console.log('Visible!')
    debugstate = false
  };
}