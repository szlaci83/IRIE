// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
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
SERVER_HOST = 'http://46.101.25.210'
UNI_HOST = 'http://10.4.175.99'
PORT = ':4444'
LOCATIONENDPOINT = '/location'
EVENTENDPOINT = '/event'
DETAILEDENDPOINT = '/emotion?location=TEST&event=Tom and Jerry&from=1522168131&to=1522168200'

LOC_URL = SERVER_HOST + PORT + LOCATIONENDPOINT
EVENT_URL = SERVER_HOST + PORT + EVENTENDPOINT
DET_URL = SERVER_HOST + PORT + DETAILEDENDPOINT

$( document ).ready(function() {

    // populate location button
  var loc_settings = {
    "async": true,
    "crossDomain": true,
    "url": LOC_URL,
    "method": "GET",
    "headers": {
      "content-type": "application/json",
      "cache-control": "no-cache",
    },
    //"processData": false,
  }
    console.log("calling: ", LOC_URL);
    $.ajax(loc_settings).done(function (response) {
        console.log("LOCATIONS: ", response)

        for (var key in response) {
            $('#location').append('<li><a href="#"><id=' + response[key].id + '">' + response[key].name+ '</a></li>');
        }

        $("#location li a").click(function () {
            $("#locationDropDown:first-child").text($(this).text());
            $("#locationDropDown:first-child").val($(this).text());

        })
    })});


  // Populate event button
  var event_settings = {
    "async": true,
    "crossDomain": true,
    "url": EVENT_URL,
    "method": "GET",
    "headers": {
      "content-type": "application/json",
      "cache-control": "no-cache",
    },
    //"processData": false,
  }
    console.log( "calling: ", EVENT_URL );
    $.ajax(event_settings).done(function (response) {
        console.log("EVENTS: ", response)

        for (var key in response) {
            $('#event').append('<li><a href="#"><id='+ response[key].id + '">' + response[key].name+ '</a></li>');
        }

        $("#event li a").click(function () {
            $("#eventDropDown:first-child").text($(this).text());
            $("#eventDropDown:first-child").val($(this).text());

        })

    console.log( "ready!" );


        var event_settings = {
            "async": true,
            "crossDomain": true,
            "url": DET_URL,
            "method": "GET",
            "headers": {
                "content-type": "application/json",
                "cache-control": "no-cache",
            },
            //"processData": false,
        }
        console.log( "calling: ", DET_URL );
        $.ajax(event_settings).done(function (response) {
            console.log("EMOTIONS: ", response)
            var time = []
            var angry  =[]
            var disgust =[]
            var fear = []
            var happy = []
            var sad = []
            var surprise = []
            var neutral=[]
          for(var res in response){
              res = response [res]
              var utcSeconds = res['timestamp'];
              var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
              d.setUTCMilliseconds(utcSeconds);
              console.log(d)
              time.push(d)
              angry.push(res['angry'])
              disgust.push(res['disgust'])
              fear.push(res['fear'])
              happy.push(res['happy'])
              sad.push(res['sad'])
              surprise.push(res['surprise'])
              neutral.push(response['neutral'])
          }



            // -- Bar Chart Example
            var ctx = document.getElementById("myLineChart");
            var myLineChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: time,
                    datasets: [{
                        label: "Revenue",
                        backgroundColor: "rgba(2,117,216,1)",
                        borderColor: "rgba(2,117,216,1)",
                        data: happy,
                    }],
                },
                options: {
                    scales: {
                        xAxes: [{
                            time: {
                                unit: 'second'
                            },
                            gridLines: {
                                display: false
                            },
                            ticks: {
                                maxTicksLimit: 6
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: 1,
                                maxTicksLimit: 5
                            },
                            gridLines: {
                                display: true
                            }
                        }],
                    },
                    legend: {
                        display: false
                    }
                }
            });

        })



});

$("#days li a").click(function(){
    $("#daysDropdownMenu:first-child").text($(this).text());
    $("#daysDropdownMenu:first-child").val($(this).text());
});
//
//
//     .click(function(){
//     var event_settings = {
//         "async": true,
//         "crossDomain": true,
//         "url": DET_URL,
//         "method": "GET",
//         "headers": {
//             "content-type": "application/json",
//             "cache-control": "no-cache",
//         },
//         //"processData": false,
//     }
//     console.log( "calling: ", DET_URL );
//     $.ajax(event_settings).done(function (response) {
//         console.log("EMOTIONS: ", response)
//
//         })
//
// })
//
//
