function set_date_time() {
    $('div#time').html(moment().format('LTS'));
    $('div#date').html(moment().format('dddd [-] MMMM Do [-] YYYY'))
    var t = setTimeout(set_date_time, 500);
}


$(document).ready(function() {
    set_date_time();
});