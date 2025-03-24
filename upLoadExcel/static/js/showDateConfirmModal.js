
(function () {
  'use strict';

  var forms = document.querySelectorAll('.needs-validation');
  console.log("Forms found:", forms);

  Array.prototype.slice.call(forms)
      .forEach(function (form) {
          form.addEventListener('submit', function (event) {
              console.log("Form submitted");
              if (!form.checkValidity()) {
                  console.log("Form is invalid");
                  event.preventDefault();
                  event.stopPropagation();
              } else {
                  console.log("Form is valid");
              }

              form.classList.add('was-validated');
          }, false);
      });
})();


document.addEventListener("DOMContentLoaded", function () {
  // Function to show a modal if there's a valid message inside it
  function showModal(modalId, logMessage) {
      var modal = document.getElementById(modalId);
      if (modal && modal.querySelector(".modal-body p").textContent.trim() !== "") {
          new bootstrap.Modal(modal).show();
          console.log(logMessage);
          return true; // Stops further modal checks
      }
      return false;
  }

  // Prioritize showing modals based on the conditions
  if (showModal('myModalNoData', "No Data modal displayed")) return;
  if (showModal('myModalMessage', "Confirmation modal displayed")) return;
  if (showModal('myModalDataRemoved', "Data Removed modal displayed")) return;

});

// Function to handle redirection after Data Removed modal is closed
function redirectAfterClose() {
  var dataRemovedModal = document.getElementById('myModalDataRemoved');
  
  // Check if the modal exists and retrieve the data-redirect attribute
  if (dataRemovedModal) {
    var redirectUrl = dataRemovedModal.getAttribute("data-redirect");
    if (redirectUrl) {
      // Redirect to the URL
      window.location.href = redirectUrl;
    }
  }
}

// Add event listener for the 'hidden.bs.modal' event, which fires when the modal is fully closed
var dataRemovedModal = document.getElementById('myModalDataRemoved');
if (dataRemovedModal) {
  dataRemovedModal.addEventListener("hidden.bs.modal", redirectAfterClose);
}






  