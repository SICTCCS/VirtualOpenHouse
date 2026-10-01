let slideIndex = 1;
const door = document.getElementById("DoorModal");
const doorButton = document.getElementById("DoorButton");
const closeDoor = document.getElementById("closeDoor");
const faq = document.getElementById("FAQModal");
const faqButton = document.getElementById("FAQButton");
const closeFAQ = document.getElementById("closeFAQ");
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("my-slides");
  let dots = document.getElementsByClassName("dot");
  if (!slides.length) return;
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

function showDoor() {
  if (door) {
    door.showModal();
  }
}

function closeOutDoor() {
  if (door) {
    door.close();
  }
}

// Close when the area outside the popup is clicked.
if (door) {
  door.onclick = function(event) {
    if (event.target !== door) return;

    let bounds = door.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom) {
      closeOutDoor();
    }
  };
}


function showFAQ() {
  if (faq) {
    faq.showModal();
  }
}

function closeOutFAQ() {
  if (faq) {
    faq.close();
  }
}

// Close when the area outside the popup is clicked.
if (faq) {
  faq.onclick = function(event) {
    if (event.target !== faq) return;

    let bounds = faq.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom) {
      closeOutFAQ();
    }
  };
}
