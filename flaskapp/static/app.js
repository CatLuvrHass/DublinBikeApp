let map;

function initMap() {

    fetch("/stations").then(response => {
        return response.json();


    }).then(data => {
        //console.log("data: ", data);

    map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 53.349804, lng: -6.260310},
      zoom: 14,
    });

    data.forEach(stations => {
        if(stations.available_bikes > 0){
            let cityCircleAvail = new google.maps.Circle({
              strokeColor: "#00CC00",
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: "#00CC00",
              fillOpacity: 0.35,
              map,
              center: { lat: stations.pos_lat, lng: stations.pos_lng },
              radius: 50,
        });
        } else if(stations.available_bikes < 5){
            let cityCircleAlmost = new google.maps.Circle({
              strokeColor: "#ffa500",
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: "#ffa500",
              fillOpacity: 0.35,
              map,
              center: { lat: stations.pos_lat, lng: stations.pos_lng },
              radius: 50,
            });
        } else {
            let cityCircleNotAvail = new google.maps.Circle({
              strokeColor: "#FF0000",
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: "#FF0000",
              fillOpacity: 0.35,
              map,
              center: { lat: stations.pos_lat, lng: stations.pos_lng },
              radius: 50,
            });
        }

        const marker = new google.maps.Marker({
            position: { lat: stations.pos_lat, lng: stations.pos_lng },
            map: map,


        });

        marker.addListener("click", () => {
            const infowindow = new google.maps.InfoWindow({

                content: '<h3>'+stations.name+'</h3><p> Available Stands: '+stations.available_bike_stands+
                '<br>Available Bikes: '+stations.available_bikes+'</p>',

            });
            infowindow.open(map,marker);
        });


    });

    }).catch(err => {
      console.log("OOPS!", err);
    });
}