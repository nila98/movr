/*
$(function() {
  $('#findcommon').click(function() {
    $.ajax({
      url: '/commonmovie.php',
      success: function(data) {
        console.log('woot worked ' + data);
      });
    });
  });
});
*/

$(function() {
  $('#commonmovie-alert').hide();
  $('#btnfindcommon').click(function() {
    $.ajax({
      url: '/commonmovie',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        console.log('commonmovie success');
        if (response == 'success') {
          window.location = '/';
        } else {
          $('#commonmovie-alert').show();
          $('#commonmovie-alert').attr('class', 'alert alert-danger');
          $('#commonmovie-alert').text(response);
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});

