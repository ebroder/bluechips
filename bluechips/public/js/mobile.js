try {
    console.log("init");
} catch(e) {
    console = { log: function() {} };
}

$(function() {
    console.log("ready()");

    $('#tabs a').click(function() {
        $('#tabs a').removeClass('selected');
        $(this).addClass('selected');
        $('div.tab').hide();

        /* See if that tab has been rendered to the page. */
        tabname = '#tab-' + $(this).attr('id');
        tab = $(tabname);
        if(tab.children().length < 1) {
            /* If not, return true so that we actually reload. */
            tab.load($(this).attr('href') + ' ' + tabname + '> *');
        }
        tab.show();
        return false;
    });
    $('#tabs a.selected').click();

    console.log("ready() done");
});

