var root = 'http://control-tea.herokuapp.com';

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
    })

    navigator.geolocation.getCurrentPosition(function(position) {
        $.get(root + '/weather?lat=' + position.coords.latitude + '&lon=' + position.coords.longitude).done(
            function(data) {
                var icon_name = data['icon'];
                console.log(icon_name.toUpperCase())
                skycons.remove("weather_icon");
                skycons.add("weather_icon", Skycons[icon_name.toUpperCase().replace('-', '_')]);
                chrome.storage.local.set({'latest_weather_icon': icon_name});
                skycons.play();
            }
        )
    })
}

function get_user_location() {

}

$(document).ready(function() {
    set_date_time();
    set_current_icon();
    get_user_location();
});