let currentSlide = 1;
const totalSlides = 5;

function showSlide(newSlide) {
    // Get elements for current and next slide
    const currentEl = document.getElementById(`slide${currentSlide}`);
    const nextEl = document.getElementById(`slide${newSlide}`);

    // Start slide-out animation on the current slide
    currentEl.classList.add('slide-out');

    // After the slide-out animation, remove the current slide
    setTimeout(() => {
        currentEl.classList.remove('active', 'slide-out');
        
        // Show next slide and start slide-in animation
        nextEl.classList.add('active', 'slide-in');
        
        // Remove the slide-in class after animation completes
        setTimeout(() => {
            nextEl.classList.remove('slide-in');
        }, 500);
        
        // Update the current slide index
        currentSlide = newSlide;
    }, 500); // This delay should match the CSS animation duration
}

function nextSlide() {
    // Calculate next slide number
    let nextSlideNum = (currentSlide % totalSlides) + 1;
    showSlide(nextSlideNum);
}

// Initial display: make sure the first slide is active without animation
document.getElementById(`slide${currentSlide}`).classList.add('active');

// Change slide every 3 seconds
setInterval(nextSlide, 3000);
