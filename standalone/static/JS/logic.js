function titleCase(str) {
    str = str.toLowerCase().split(' ');
    for (var i = 0; i < str.length; i++) {
        str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
    }
    return str.join(' ');
}
function lineMaker(e) {
    let countryName = e.target.feature.properties.ADMIN
    let countryValues = e.target.feature.properties.values
    let countryCorrelation = e.target.feature.properties.correlation
    console.log(countryName)
    console.log(countryValues)
    console.log(countryCorrelation)

    var trace1 = {
        x: years,
        y: elon,
        type: 'scatter',
        name: 'Elon Tweets'
    };

    var trace2 = {
        x: years,
        y: countryValues,
        yaxis: 'y2',
        type: 'scatter',
        name: responseVar
    };

    var data = [trace1, trace2];

    var layout = {
        title: `Elon's Tweets vs ${responseVar} in ${countryName}`,
        yaxis: { title: '# of Tweets' },
        yaxis2: {
            title: responseVar,
            titlefont: { color: 'rgb(148, 103, 189)' },
            tickfont: { color: 'rgb(148, 103, 189)' },
            //anchor:  'free',
            overlaying: 'y',
            side: 'right'
        },
        legend: {
            x: .05,
            overlaying: 'y',
            font: {
                size: 13
            }
        }
    };

    Plotly.newPlot("line", data, layout);
}

function new_response(respo) {
    var tweet = tweets[Math.floor(Math.random()*tweets.length)]
    responseVar = titleCase(respo)
    shapes.features.sort(function (a, b) {
        return b.properties[respo].correlation - a.properties[respo].correlation
    })
    topTenCorrelations = shapes.features.slice(0, 10).map(function (x) {
        return x.properties[respo].correlation
    })
    topTenCountries = shapes.features.slice(0, 10).map(function (x) {
        return x.properties.ADMIN
    })
    var trace1 = {
        type: "bar",
        orientation: "h",
        x: topTenCorrelations,
        y: topTenCountries,
        text: topTenCountries,
    };

    var data = [trace1];

    var layout1 = {
        title: `Top Ten Correlations <br> for ${responseVar}`,
    };

    Plotly.newPlot("bar", data, layout1)

    var trace1 = {
        x: years,
        y: elon,
        type: 'scatter',
        name: 'Elon Tweets'
    };
    
    var data = [trace1];
    
    var layout = {
        title: `# of Elons Tweets`,
        yaxis: { title: '# of Tweets' },
        yaxis2: {
            title: responseVar,
            titlefont: { color: 'rgb(148, 103, 189)' },
            tickfont: { color: 'rgb(148, 103, 189)' },
            //anchor:  'free',
            overlaying: 'y',
            side: 'right'
        },
        legend: {
            x: .05,
            overlaying: 'y',
            font: {
                size: 13
            }
        }
    };
    
    Plotly.newPlot("line", data, layout);
    
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
        scale: ["orange", "green"],
    
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
        onEachFeature: function (feature, layer) {
            layer.bindPopup(`<h4>${feature.properties.ADMIN}</h4> Correlation: ${feature.properties.correlation}`);
            layer.on({
                click: lineMaker
            })
        }
    }).addTo(myMap);
    
    // Set up the legend
    var legend = L.control({ position: "bottomright" });
    legend.onAdd = function () {
        var div = L.DomUtil.create("div", "info legend");
        var limits = geojson.options.limits;
        var colors = geojson.options.colors;
        var labels = [];
    
        // Add min & max
        var legendInfo = `<h3>${responseVar} Correlation</h3>` +
            "<div class=\"labels\">" +
            "<div class=\"min\">" + limits[0] + "</div>" +
            "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
            "</div>";
    
        div.innerHTML = legendInfo;
    
        limits.forEach(function (_limit, index) {
                labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
            });
    
        div.innerHTML += "<ul>" + labels.join("") + "</ul>";
        return div;
    };
    legend.addTo(myMap);
}


// Adding legend to the map




new_response("happiness")


