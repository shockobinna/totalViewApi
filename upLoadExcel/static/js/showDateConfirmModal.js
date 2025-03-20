

document.addEventListener("DOMContentLoaded", function () {
    // Check if the modal exists on the page (it will exist only if there is a message)
    var modal = document.getElementById('myModal');
    
    if (modal) {
      // Show the modal only if it exists and contains a message
      $('#myModal').modal('show');
      console.log("called modal")
    }
  
    // Optionally, you can focus on an input or other element if needed inside the modal
    // $('#myModal').on('shown.bs.modal', function () {
    //   // Focus on an input field inside the modal if you need (optional)
    //   $('#myInput').trigger('focus'); // Uncomment if you have an element with id="myInput"
    // });
  });
  