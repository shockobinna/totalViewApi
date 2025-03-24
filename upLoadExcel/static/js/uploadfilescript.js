// Function to close error block (alert + table)
function closeErrorAndTable() {
    var errorBlock = document.getElementById('errorBlock');
    if (errorBlock) {
        errorBlock.style.display = 'none';
    }
}


// Function to manually close success message with fade-out and redirect
function closeSuccessMessage() {
    var successMessage = document.getElementById('successMessage');
    var redirectUrl = successMessage.dataset.redirect; // Get redirect URL from the data attribute

    console.log("Redirect URL: " + redirectUrl); // Log the URL to ensure it's correct

    if (successMessage && redirectUrl) {
        successMessage.classList.remove('show'); // Bootstrap fade-out class
        setTimeout(function () {
            successMessage.style.display = 'none'; // Hide after fade-out
            console.log("Redirecting to: " + redirectUrl); // Log the redirect before actually doing it
            window.location.href = redirectUrl; // Redirect after closing the message
        }, 500); // 500ms delay to match fade-out transition
    } else {
        console.log("Error: Missing redirect URL or success message."); // Error if URL is not found
    }
}


// Auto-close success message after 10 seconds with fade-out and redirect
window.onload = function () {
    var successMessage = document.getElementById('successMessage');
    var redirectUrl = successMessage ? successMessage.dataset.redirect : ''; // Get redirect URL from the data attribute
    if (successMessage) {
        setTimeout(function () {
            successMessage.classList.remove('show'); // Bootstrap fade-out
            setTimeout(function () {
                successMessage.style.display = 'none'; // Hide after fade
                window.location.href = redirectUrl; // Redirect after message is hidden
            }, 1000); // 500ms to match fade duration
        }, 10000); // Auto-close after 10 seconds
    }
};


document.addEventListener('DOMContentLoaded', function () {
    // Select form and spinner
    const form = document.getElementById('uploadForm');
    const spinner = document.getElementById('loadingSpinner');

    // Show spinner on form submit
    form.addEventListener('submit', function () {
        spinner.style.display = 'flex'; // Show spinner when form is submitted
    });

    // Always hide spinner on page load in case of reload or redirect
    spinner.style.display = 'none';
});


