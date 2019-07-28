<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-sclae=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>My Google Maps</title>
    <style>
      #map{
        height:400px;
        width:100%;
      }
    </style>
  </head>
  <body>
      <h1>My Google Map</h1>
      <div id="map"></div>
      <script>
        function initMap(){
          //Map options, use 13 for city of detroit
          var options = {
            zoom:15,
            center:{lat:42.3314,lng:-83.0458}
          }

          //New Map
          var map = new google.maps.Map(document.getElementById('map'), options);


          //Add marker
          var marker = new google.maps.Marker({
            position:{lat:42.3314,lng:-83.0458},
            map:map,
            icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
          });

          var infoWindow = new google.maps.InfoWindow({
            content:'<h1>Detroit MI</h1>'
          });

          marker.addListener('click', function(){
            infoWindow.open(map, marker);
          });
        }
    </script>


    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB0sS5_Rtq-AKDMRTUp0zbO4_s3h79QnNE&callback=initMap"
    async defer></script>
  </body>
</html>
