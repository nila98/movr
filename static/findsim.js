$(function() {
  $('#findsim-alert').hide();
  $('#btnfindsim').click(function() {
    $.ajax({
      url: '/findsim',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        if (response == 'success') {
        } else {
          $('#findsim-alert').show();
          $('#findsim-alert').attr('class', 'alert alert-danger');
          $('#findsim-alert').text(response);
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});

