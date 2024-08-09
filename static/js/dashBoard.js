let currentSlide = 1;
const totalSlides = 5;

function showSlide(slideNumber) {
    // Hide all slides
    for (let i = 1; i <= totalSlides; i++) {
        document.getElementById(`slide${i}`).classList.remove('active');
    }
    // Show the current slide
    document.getElementById(`slide${slideNumber}`).classList.add('active');
}

function nextSlide() {
    currentSlide = (currentSlide % totalSlides) + 1;
    showSlide(currentSlide);
}

// Initial display
showSlide(currentSlide);

// Change slide every 5 seconds
setInterval(nextSlide, 3000);
