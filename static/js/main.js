// Main JavaScript for Shiny Quiz

document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            // Send AJAX request to toggle theme
            fetch('/theme/toggle/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle the theme
                    const html = document.documentElement;
                    if (data.dark_mode) {
                        html.setAttribute('data-bs-theme', 'dark');
                        themeToggle.innerHTML = '<i class="bi bi-sun"></i>';
                    } else {
                        html.removeAttribute('data-bs-theme');
                        themeToggle.innerHTML = '<i class="bi bi-moon"></i>';
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Quiz timer functionality
    const quizTimer = document.getElementById('quiz-timer');
    if (quizTimer) {
        const timeLimit = parseInt(quizTimer.dataset.timeLimit, 10);
        if (timeLimit > 0) {
            let timeLeft = timeLimit * 60; // Convert to seconds
            
            const timerInterval = setInterval(function() {
                timeLeft--;
                
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                
                quizTimer.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
                
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    document.getElementById('quiz-form').submit();
                }
            }, 1000);
        }
    }
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}