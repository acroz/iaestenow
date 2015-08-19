
var map;

function initialize() {
 
  // Initialise map
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 6,
    center: {lat: 51.5072, lng: 0} // Default centre on London
  });

  //centre_current_position();
  ajax_centre_on_address('Göttingen');
  //ajax_mark_address('Graz');
  //ajax_mark_address('Utrecht');
  //ajax_mark_address('London, UK');
  ajax_load_entries();

}

function add_marker(title, type, latitude, longitude) {
  var pos = new google.maps.LatLng(latitude, longitude);
  var marker_info = {
    title: title,
    map: map,
    position: pos
  };
  if (type == 'user_location')
    marker_info['icon'] = {
      // https://developers.google.com/maps/documentation/javascript/symbols#predefined
      // https://developers.google.com/maps/documentation/javascript/reference#Symbol
      path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
      scale: 6,
      fillColor: 'lightblue',
      fillOpacity: 1,
      strokeWeight: 2
    };
  var marker = new google.maps.Marker(marker_info);
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
      centre(data.latitude, data.longitude);
    }
  );
}

function ajax_mark_address(address) {
  $.getJSON(
    $SCRIPT_ROOT + "/geocode",
    {'address': address},
    function (data) {
      add_marker(address, 'address', data.latitude, data.longitude);
    }
  );
}

function ajax_load_entries() {
  $.getJSON(
    $SCRIPT_ROOT + "/entries",
    {},
    function (data) {
      $.each(data.response, function(index, entry) {
        add_marker(entry.name, entry.type, entry.latitude, entry.longitude);
      })
    }
  );
}

google.maps.event.addDomListener(window, 'load', initialize);
