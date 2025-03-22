
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
  var noDataModal = document.getElementById('myModalNoData');
  var messageModal = document.getElementById('myModalMessage');

  // Check if the modal exists and contains meaningful content
  if (noDataModal && noDataModal.querySelector(".modal-body p").textContent.trim() !== "") {
      var modalInstance = new bootstrap.Modal(noDataModal);
      modalInstance.show();
      console.log("No Data modal displayed");
  } else if (messageModal && messageModal.querySelector(".modal-body p").textContent.trim() !== "") {
      var modalInstance = new bootstrap.Modal(messageModal);
      modalInstance.show();
      console.log("Confirmation modal displayed");
  }
});



  