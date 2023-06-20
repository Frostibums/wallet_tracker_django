function openTab(evt, wallet, chain) {
  // Declare all variables
  var i, tabcontent, tablinks;
  var wallet_chain;
  wallet_chain = wallet + '-' + chain;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementById(wallet).getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].setAttribute('style', 'display:none');
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and toggle an "active" class to the button that opened the tab
  document.getElementById(wallet_chain).setAttribute('style', 'display:flex');
  evt.currentTarget.classList.toggle("active");
}