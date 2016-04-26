// var map;
// function initMap() {
//   map = new google.maps.Map(document.getElementById('map'), {
//     center: {lat: -37.48, lng: 144.57}, 
//     zoom: 8
//   });
// }

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -25, lng: 133},
    zoom: 4
  });

  var layer = new google.maps.FusionTablesLayer({
    query: {
      select: 'geometry',
      from: '1SLBrU0TyK4PRtHO5GOeFjNAPV-npESHICtcclPHU'
    },
    styles: [{
      polygonOptions: {
        fillColor: '#0000C6',
        fillOpacity: 0.3
        }
      }, {
        where: 'Population > 10000000',
        polygonOptions: {
        fillColor: '#FF0000',
        fillOpacity: 0.3
        }
      }, {
        where: 'Population > 1000000',
        polygonOptions: {
        fillColor: '#007979',
        fillOpacity: 0.3
        }
      }, {
        where: 'Population > 5000000',
        polygonOptions: {
        fillColor: '#2894FF',
        fillOpacity: 0.3
        }
      }]
  });
  layer.setMap(map);
}

// var map;
// function initMap() {
//   map = new google.maps.Map(document.getElementById('map'), {
//     center: {lat: -37.48, lng: 144.57}, 
//     zoom: 8
//   });
// }

// function initMap() {
//   var map = new google.maps.Map(document.getElementById('map'), {
//     center: {lat: -25, lng: 133},
//     zoom: 4
//   });

//   var layer = new google.maps.FusionTablesLayer({
//     query: {
//       select: 'geometry',
//       from: '1SLBrU0TyK4PRtHO5GOeFjNAPV-npESHICtcclPHU'
//     },
//     styles: [{
//       polygonOptions: {
//         fillColor: '#00FF00',
//         fillOpacity: 0.3
//       }
//     }, {
//       where: 'birds > 300',
//       polygonOptions: {
//         fillColor: '#0000FF'
//       }
//     }, {
//       where: 'population > 5',
//       polygonOptions: {
//         fillOpacity: 1.0
//       }
//     }]
//   });
//   layer.setMap(map);
// }