$(function() {

	// Floating label headings for the contact form
	$(function() {
		  $("body").on("input propertychange", ".floating-label-form-group", function(e) {
		      $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
		  }).on("focus", ".floating-label-form-group", function() {
		      $(this).addClass("floating-label-form-group-with-focus");
		  }).on("blur", ".floating-label-form-group", function() {
		      $(this).removeClass("floating-label-form-group-with-focus");
		  });
	});
  $('#signup-alert').hide();
  $('#btnSignUp').click(function() {
    $.ajax({
      url: '/showsignup',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        if (response == 'success') {
          window.location = '/';
        } else {
          $('#signup-alert').show();
          $('#signup-alert').attr('class', 'alert alert-danger');
          $('#signup-alert').text(response);
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
}); // End of use strict

