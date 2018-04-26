SERVER_HOST = 'http://46.101.25.210'
UNI_HOST = 'http://10.4.175.99'
PORT = ':4444'
ENDPOINT = '/location'
URL = SERVER_HOST + PORT + ENDPOINT

function showAlert(message) {
    $('#alert').html("<div class='alert alert-success'>"+message+"</div>");
    $('#alert').show().fadeTo(2000, 500).slideUp(500, function(){
        $("#alert").slideUp(500);
    });;
}
$(document).ready(function() {
    $('form').submit(function(event) {
        console.log($('input[name=name]').val())
        console.log($('input[name=address]').val())
        console.log($('input[name=city]').val())
        console.log($('input[name=postalcode]').val())
        var formData = {
            name: $('input[name=name]').val(),
            address: $('input[name=addressl1]').val() +
            $('input[name=addressl2]').val() +
            $('input[name=city]').val() +
            $('input[name=postalcode]').val()
        };

        console.log("calling: ", URL);

          var settings = {
                "async": true,
                "crossDomain": true,
                "url": URL,
                "data" : JSON.stringify(formData),
                "type": "POST",
                "dataType" : "json",
                "headers": {
                        "content-type": "application/json",
                        "cache-control": "no-cache",
                },
        "processData": false
    }
        $.ajax(settings)
            .done(function(data) {
                console.log(data)
                showAlert("New location saved!")
            });
         event.preventDefault();
    });

});

