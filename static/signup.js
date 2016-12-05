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

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: {lat: -34.397, lng: 150.644}
  });
  var geocoder = new google.maps.Geocoder();

  document.getElementById('submit').addEventListener('click', function() {
    geocodeAddress(geocoder, map);
  });
}

function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}
