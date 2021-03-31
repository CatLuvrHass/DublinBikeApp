let map;
let another;
function initMap() {

    // const directionsService = new google.maps.DirectionsService();
    // const directionsRenderer = new google.maps.DirectionsRenderer();

    fetch("/stations").then(response => {
        return response.json();


    }).then(data => {
        // console.log("data: ", data);

    map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 53.349804, lng: -6.260310},
      zoom: 14,
    });
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    const onChangeHandler = function () {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
    };
    document.getElementById("start").addEventListener("change", onChangeHandler);
    document.getElementById("end").addEventListener("change", onChangeHandler);


    data.forEach(stations => {
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

    citySelect();

    }).catch(err => {
      console.log("OOPS!", err);
    });
}


function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  directionsService.route(
    {
      origin: {
        query: document.getElementById("start").value,
      },
      destination: {
        query: document.getElementById("end").value,
      },
      travelMode: google.maps.TravelMode.DRIVING,
    },
    (response, status) => {
      if (status === "OK") {
        directionsRenderer.setDirections(response);
      } else {
        window.alert("Directions request failed due to " + status);
      }
    }
  );
}

function citySelect(){

    const start_ele = document.getElementById('start');
    const end_ele = document.getElementById('end');
    fetch("/stations").then(result => {
        return result.json();
    }).then(another => {
        // console.log("anotherone: ", another);
            another.forEach(station =>{
                const post_lat = station.pos_lat;
                const post_lng = station.pos_lng;
                const stationLatLng = { lat: post_lat, lng: post_lng };
                console.log(stationLatLng);
                start_ele.innerHTML = start_ele.innerHTML +
                '<option value="' + station.name + ", Dublin, Ireland" + '">' + station.name + '</option>';
                end_ele.innerHTML = end_ele.innerHTML +
                '<option value="' +  station.name+ ", Dublin, Ireland" + '">' + station.name + '</option>';
                const selectedStation = document.getElementById("start");
                console.log(selectedStation);
        //
        // console.log(station.name);
    });
    });
}
