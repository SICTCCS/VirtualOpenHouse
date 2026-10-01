function openTab(evt, tabName) {
  // Get all elements with class="tab-content" and hide them
  const contents = document.getElementsByClassName("tab-content");
  for (let i = 0; i < contents.length; i++) {
    contents[i].classList.remove("active");
  }

  // Get all elements with class="tab-btn" and remove "active"
  const buttons = document.getElementsByClassName("tab-btn");
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove("active");
  }

  // Show the specific current tab and add an "active" class to the button
  document.getElementById(tabName).classList.add("active");
  evt.currentTarget.classList.add("active");
}