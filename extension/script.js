var root = 'http://control-tea.herokuapp.com';
// var root = 'http://127.0.0.1:5000';

function set_date_time() {
    $('div#time').html(moment().format('LTS'));
    $('div#date').html(moment().format('dddd [-] MMMM Do [-] YYYY'))
    var t = setTimeout(set_date_time, 500);
}

function set_current_icon() {
    var skycons = new Skycons({"color": "white"});
    // cached icon
    chrome.storage.local.get('latest_weather_icon', function (cached_icon) {
        if (cached_icon) {
            skycons.add("weather_icon", cached_icon['latest_weather_icon']);
        }

        navigator.geolocation.getCurrentPosition(function(position) {
            $.get(root + '/weather?lat=' + position.coords.latitude + '&lon=' + position.coords.longitude).done(
                // TODO: handle cases when position is unavailable
                function(data) {
                    console.log(data);
                    var icon_name = data['icon'].toUpperCase().replace(/-/g, '_');
                    var current_temp = data['current_temp']
                    $('#current_temp').html(current_temp + '°');
                    if (icon_name != cached_icon) {
                        console.log('new icon');
                        skycons.remove("weather_icon");
                        skycons.add("weather_icon", Skycons[icon_name]);
                        chrome.storage.local.set({'latest_weather_icon': icon_name});
                    }
                    skycons.play();
                }
            )
        })
    })
}

$(document).ready(function() {
    set_date_time();
    set_current_icon();
});