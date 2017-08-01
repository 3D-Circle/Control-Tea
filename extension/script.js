var root = 'http://control-tea.herokuapp.com';
// var root = 'http://127.0.0.1:5000';

/* Date & time */
function set_date_time() {
    $('div#time').html(moment().format('LTS'));
    $('div#date').html(moment().format('dddd [-] MMMM Do [-] YYYY'))
    var t = setTimeout(set_date_time, 500);
}

/* Weather icon */
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



/* Sidebar */
var new_width;
var sidebar_toggled = false;
var left_angle_quote = '&lsaquo;'
var right_angle_quote = '&rsaquo;'
var sidebar_width = 350;
function toggle_sidebar() {
    /* expands or hides sidebar depending on current sidebar state */
    new_width = sidebar_width * (sidebar_toggled ? 0 : 1);
    $('#sidebar').css('width', new_width + 'px');
    $('#sidebar_blur').css('width', new_width + 'px');
    $('#sidebar_toggle').css('right', new_width + 'px');
    /* switch arrow indicator depending on sidebar state */
    $('#sidebar_toggle').html(sidebar_toggled ? left_angle_quote : right_angle_quote);
    sidebar_toggled = !sidebar_toggled;
}


/* Widgets in sidebar */
function set_lichess_puzzle() {
    $('#widgets').append("<div class='widget_title'>Daily puzzle</div>")
    $('#widgets').append("<div style='text-align:center;'><iframe src='https://lichess.org/training/frame?bg=dark&theme=brown' class='lichess-training-iframe' allowtransparency='true' frameBorder='0' style='width: 224px; height: 264px; display:inline-block;' title='Lichess free online chess'></iframe></div>")
}

/*
  Settings
*/
settings_default = {
    widgets: ['lichess'],
    bg: {
        islocal: false,
        path: 'http://www.nationalgeographic.com/content/dam/photography/PROOF/2017/April/epic-landscapes/16-9154838_uploadsmember516662yourshot-516662-9154838jpg_ekc3qcvrtc4diwvyxwqwxf74bezxs2udwatjavjxeftgooyp4jfa_5760x3840.ngsversion.1492194605387.adapt.1190.1.jpg'
    }
}

function apply_settings() {
    var user_settings;
    chrome.storage.sync.get('saved_settings', function (saved_settings) {
        if (saved_settings.length) {
            user_settings = saved_settings;  
        } else {
            user_settings = settings_default;
        }
        /* populate sidebar with widgets */
        for (var i = 0; i < user_settings['widgets'].length; i++) {
            current = user_settings['widgets'][i];

            switch (current) {
                case 'lichess':
                    set_lichess_puzzle();
                    break;
            }
            $('#widgets').append('<hr>')
        }
        /* add settings at the bottom of the sidebar */
        
        /* configure bg pic */
        if (user_settings['bg']['islocal']) {
            
        } else {
            $('body').css('background',  "url('" + user_settings['bg']['path'] + "') no-repeat center center fixed");
        }
        $('body').css('background-size', 'cover');
    })
}

                             
$(document).ready(function() {
    $("#sidebar_toggle").click(toggle_sidebar);
    
    set_date_time();
    set_current_icon();
    apply_settings();
//    set_settings();
    
    chrome.commands.onCommand.addListener(function (command) {
        switch(command) {
            case 'toggle_sidebar':
                toggle_sidebar();
                break;
        }
    });
});