
var map;

function initialize() {
 
  // Initialise map
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 6,
    center: {lat: 51.5072, lng: 0} // Default centre on London
  });

  //centre_current_position();
  ajax_centre_on_address('Prague');
  //ajax_mark_address('Graz');
  //ajax_mark_address('Utrecht');
  ajax_mark_address('London, UK');
  ajax_load_entries();

}

function add_marker(title, latitude, longitude) {
  var pos = new google.maps.LatLng(latitude, longitude);
  var marker = new google.maps.Marker({
    title: title,
    map: map,
    position: pos
  });
}

function centre(latitude, longitude) {
  var pos = new google.maps.LatLng(latitude, longitude);
  map.setCenter(pos)
}

function centre_current_position() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude,
                                       position.coords.longitude);
      map.setCenter(pos);
    }, function() {
      // Do nothing
      // handleNoGeolocation(true);
    });
  }
}

function ajax_centre_on_address(address) {
  $.getJSON(
    $SCRIPT_ROOT + "/geocode",
    {'address': address},
    function (data) {
      add_marker(address, data.latitude, data.longitude);
      centre(data.latitude, data.longitude);
    }
  );
}

function ajax_mark_address(address) {
  $.getJSON(
    $SCRIPT_ROOT + "/geocode",
    {'address': address},
    function (data) {
      add_marker(address, data.latitude, data.longitude);
    }
  );
}

function ajax_load_entries() {
  $.getJSON(
    $SCRIPT_ROOT + "/entries",
    {},
    function (data) {
      $.each(data.response, function(index, entry) {
        add_marker(entry.name, entry.latitude, entry.longitude);
      })
    }
  );
}

google.maps.event.addDomListener(window, 'load', initialize);
