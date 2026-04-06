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
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
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
  door.style.display = 'block';
  console.log("Showing Door...");
}
 function closeOutDoor() {
   door.style.display = 'none';
   console.log("Closing Door...");
}


function showFAQ() {
  faq.style.display = 'block';
  console.log("Showing FAQ...");
}
 function closeOutFAQ() {
   faq.style.display = 'none';
   console.log("Closing FAQ...");
}