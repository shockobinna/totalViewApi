// Function to close error block (alert + table)
function closeErrorAndTable() {
    var errorBlock = document.getElementById('errorBlock');
    if (errorBlock) {
        errorBlock.style.display = 'none';
    }
}

// Function to manually close success message with fade-out
function closeSuccessMessage() {
    var successMessage = document.getElementById('successMessage');
    if (successMessage) {
        successMessage.classList.remove('show'); // Bootstrap fade-out
        setTimeout(function () {
            successMessage.style.display = 'none'; // Hide after fade-out
        }, 500); // 500ms for fade transition
    }
}

// Auto-close success message after 10 seconds with fade-out
window.onload = function () {
    var successMessage = document.getElementById('successMessage');
    if (successMessage) {
        setTimeout(function () {
            successMessage.classList.remove('show'); // Bootstrap fade-out
            setTimeout(function () {
                successMessage.style.display = 'none'; // Hide after fade
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


