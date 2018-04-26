// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

SERVER_HOST = 'http://46.101.25.210'
UNI_HOST = 'http://10.100.16.101'
PORT = ':4444'
ENDPOINT = '/emotion/aggregated'
URL = SERVER_HOST  + PORT + ENDPOINT


$( document ).ready(function() {
    console.log( URL );
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": URL,
        "data" : {
            event : 'Tom and Jerry'
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

        // -- Pie Chart Example
        var ctx = document.getElementById("myPieChart");

        var myPieChart = new Chart(ctx, {
            type: 'pie',
            data: data,
        });

        console.log(data)

    })
});

// //-- Area Chart Example
// var ctx = document.getElementById("myAreaChart");
// var myLineChart = new Chart(ctx, {
//   type: 'line',
//   data: {
//     labels: ["Mar 1", "Mar 2", "Mar 3", "Mar 4", "Mar 5", "Mar 6", "Mar 7", "Mar 8", "Mar 9", "Mar 10", "Mar 11", "Mar 12", "Mar 13"],
//     datasets: [{
//       label: "Sessions",
//       lineTension: 0.3,
//       backgroundColor: "rgba(2,117,216,0.2)",
//       borderColor: "rgba(2,117,216,1)",
//       pointRadius: 5,
//       pointBackgroundColor: "rgba(2,117,216,1)",
//       pointBorderColor: "rgba(255,255,255,0.8)",
//       pointHoverRadius: 5,
//       pointHoverBackgroundColor: "rgba(2,117,216,1)",
//       pointHitRadius: 20,
//       pointBorderWidth: 2,
//       data: [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 38451],
//     }],
//   },
//   options: {
//     scales: {
//       xAxes: [{
//         time: {
//           unit: 'date'
//         },
//         gridLines: {
//           display: false
//         },
//         ticks: {
//           maxTicksLimit: 7
//         }
//       }],
//       yAxes: [{
//         ticks: {
//           min: 0,
//           max: 40000,
//           maxTicksLimit: 5
//         },
//         gridLines: {
//           color: "rgba(0, 0, 0, .125)",
//         }
//       }],
//     },
//     legend: {
//       display: false
//     }
//   }
// });
// // -- Bar Chart Example
// var ctx = document.getElementById("myBarChart");
// var myLineChart = new Chart(ctx, {
//   type: 'bar',
//   data: {
//     labels: ["January", "February", "March", "April", "May", "June"],
//     datasets: [{
//       label: "Revenue",
//       backgroundColor: "rgba(2,117,216,1)",
//       borderColor: "rgba(2,117,216,1)",
//       data: [4215, 5312, 6251, 7841, 9821, 14984],
//     }],
//   },
//   options: {
//     scales: {
//       xAxes: [{
//         time: {
//           unit: 'month'
//         },
//         gridLines: {
//           display: false
//         },
//         ticks: {
//           maxTicksLimit: 6
//         }
//       }],
//       yAxes: [{
//         ticks: {
//           min: 0,
//           max: 15000,
//           maxTicksLimit: 5
//         },
//         gridLines: {
//           display: true
//         }
//       }],
//     },
//     legend: {
//       display: false
//     }
//   }
// });