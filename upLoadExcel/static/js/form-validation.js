(function () {
    'use strict';

    var forms = document.querySelectorAll('.needs-validation');
    console.log(forms)

    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated');
            }, false);
        });
})();

// Function to close error block (alert + table)
function closeErrorAndTable() {
    var errorBlock = document.getElementById('errorBlock');
    if (errorBlock) {
        errorBlock.style.display = 'none';
    }
}

