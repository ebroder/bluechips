try {
    console.log("init");
} catch(e) {
    console = { log: function() {} };
}

$(function() {
    console.log("ready()");

    $('#tabs a').click(function() {
        $('div.tab').hide();
        $('#tabs a').removeClass('selected');
        $(this).addClass('selected');
        $('#tab-' + $(this).attr('id')).show();
        return false;
    });

    console.log("ready() done");
});

