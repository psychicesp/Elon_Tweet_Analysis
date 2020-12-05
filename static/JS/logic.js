//var shapes for drawing country outlines
//var elon for elon data
//var years for years
//var countries for country list
//var happy for default response variable
//vars freedom and GDP for alternate response variables
console.log(shapes)
console.log(elon)
console.log(years)

var topShapes = shapes.features.slice(0,10)
console.log(topShapes)

// Creating map object
var myMap = L.map("map", {
    center: [0, 0],
    zoom: 2
});

// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);


geojson = L.choropleth(shapes, {

    // Define what  property in the features to use
    valueProperty: "correlation",

    // Set color scale
    scale: ["orange","green"],

    // Number of breaks in step range
    steps: 10,

    // q for quartile, e for equidistant, k for k-means
    mode: "q",
    style: {
    // Border color
    //color: "white" ,
    weight: 1,
    fillOpacity: 0.6
    },

    // Binding a pop-up to each layer
    onEachFeature: function(feature, layer) {
    layer.bindPopup("Correlation: " + feature.properties.correlation + "<br>Values =<br>" +
        "$" + feature.properties.values);
    }
}).addTo(myMap);

// Set up the legend
var legend = L.control({ position: "bottomright" });
legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");
    var limits = geojson.options.limits;
    var colors = geojson.options.colors;
    var labels = [];

    // Add min & max
    var legendInfo = "<h1>Happiness Correlation</h1>" +
    "<div class=\"labels\">" +
        "<div class=\"min\">" + limits[0] + "</div>" +
        "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
    "</div>";

    div.innerHTML = legendInfo;

    limits.forEach(function(limit, index) {
    labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
    });

    div.innerHTML += "<ul>" + labels.join("") + "</ul>";
    return div;
};

// Adding legend to the map
legend.addTo(myMap);

function mycharts(response) {

    var trace1 = [{
        type: "bar",
        orientation: "h",
        x: sample_values,
        y: otu_ids.map(each => `OTU ${each}`),
        text: otu_labels,
    }];

    var trace2 = [{
        x: otu_ids2,
        y: sample_values2,
        text: otu_labels2,
        mode: 'markers',
        marker:  {
            color: otu_ids2,
            colorscale:  'Viridis',
            size: sample_values2,
        }
            
    }];

    var layout1 = {
        title: "Test Subject's Top 10 OTU's (Abundance of Species)",               
        }

    var layout2 = {
        title:  "Full Profile of Test Subject's OTU Spectrum"

    }
    
    Plotly.newPlot("bar", trace1, layout1);
    Plotly.newPlot("bubble", trace2, layout2);


}
  
  
