$(function() {
  $('#add_movie-alert').hide();
  $('#btnadd_movie').click(function() {
    $.ajax({
      url: '/add_movie',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        if (response == 'success') {
        } else {
          $('#add_movie-alert').show();
          $('#add_movie-alert').attr('class', 'alert alert-danger');
          $('#add_movie-alert').text(response);
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});

