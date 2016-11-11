$(function() {
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
});

