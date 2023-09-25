let currentIndex = 0;
const slides = document.querySelectorAll(".swiper-slide");
const slider = document.querySelector(".swiper-container");

function showSlide(index) {
  if (index < 0) {
    index = slides.length - 1;
  } else if (index >= slides.length) {
    index = 0;
  }
  slider.style.transform = `translateX(-${index * 820}px)`;
  currentIndex = index;
}

function prevSlide() {
  showSlide(currentIndex - 1);
}

function nextSlide() {
  showSlide(currentIndex + 1);
}

showSlide(currentIndex);
