// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

SERVER_HOST = 'http://46.101.25.210'
UNI_HOST = 'http://10.100.16.101'
PORT = ':4444'
ENDPOINT = '/emotion/aggregated'
URL = SERVER_HOST + PORT + ENDPOINT

$( document ).ready(function() {
    console.log("calling: ", URL );
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": URL,
        "data" : {
            event : 'Star Wars'
        },
        "method": "GET",
        "headers": {
            "content-type": "application/json",
            "cache-control": "no-cache",
        },
        //"processData": false,
    }


    $.ajax(settings).done(function (response) {
      console.log(response)
      var data = {
          labels: ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"],
          datasets: [{
              data: [response['angry'], response['disgust'], response['fear'], response['happy'], response['sad'], response['surprise'], response['neutral']],
              backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745', '#FF00FF', '#B22222', '#FF4500', '#2F4F4F'],
          }]}

        var ctx = document.getElementById("myPieChart");

        var myPieChart = new Chart(ctx, {
            type: 'pie',
            data: data,
        });
        console.log(data)
    })
});
