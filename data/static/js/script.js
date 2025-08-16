
  // Image click event to enlarge
  document.getElementById('hero-image').addEventListener('click', function() {
    this.querySelector('img').classList.toggle('scale-110');
  });

  // Heading click event to enlarge
  document.getElementById('hero-heading').addEventListener('click', function() {
    this.classList.toggle('scale-110');
  });

  // Button click event to enlarge
  document.getElementById('hero-button').addEventListener('click', function() {
    this.classList.toggle('scale-110');
  });


   // Scroll event to trigger animation when the feature enters the viewport
   const features = document.querySelectorAll('.feature-item');
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.5 });

  features.forEach(feature => {
    observer.observe(feature);
  });

  // Image, heading, and button click event to enlarge
  document.querySelectorAll('.feature-item img, .feature-item h3').forEach(item => {
    item.addEventListener('click', function() {
      this.classList.toggle('scale-110');
    });
  });

  document.querySelectorAll('.interactive-image, #interactive-heading, #interactive-button').forEach((element) => {
    element.addEventListener('click', () => {
      element.classList.add('scale-110'); // Add scale on click
      setTimeout(() => {
        element.classList.remove('scale-110'); // Remove scale smoothly
      }, 500); // Match the duration of the transition
    });
  });



  const dynamicText = [
    "Your Workflow",
    "Team Collaboration",
    "Project Management",
    "Task Automation",
    "Productivity Tools",
  ];

  let index = 0;
  let currentText = '';
  let isTyping = true;
  const element = document.getElementById("dynamic-text");

  function typeText() {
    if (isTyping) {
      currentText = dynamicText[index].slice(0, currentText.length + 1); // Add one character
      element.textContent = currentText;

      if (currentText.length === dynamicText[index].length) {
        isTyping = false;
        setTimeout(() => {
          isTyping = true;
          index = (index + 1) % dynamicText.length; // Cycle through text
          currentText = ''; // Reset text for the next cycle
        }, 1000); // Pause before moving to the next text
      }
    }
  }

  setInterval(typeText, 150); // Type every 150ms
   const themeToggleButton = document.getElementById('theme-toggle');

    // Check if the light theme is already applied in localStorage
    if (localStorage.getItem('theme') === 'light') {
      document.body.classList.add('light-theme');
    }

    // Toggle the theme on button click
    themeToggleButton.addEventListener('click', () => {
      document.body.classList.toggle('light-theme');

      // Save theme choice in localStorage
      if (document.body.classList.contains('light-theme')) {
        localStorage.setItem('theme', 'light');
        themeToggleButton.textContent = '☀️'; // Change icon to sun for light theme
      } else {
        localStorage.removeItem('theme');
        themeToggleButton.textContent = '🌙'; // Change icon to moon for dark theme
      }
    });


