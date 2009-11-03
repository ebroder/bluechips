try {
    console.log("init");
} catch(e) {
    console = { log: function() {} };
}

$(function() {
    console.log("ready()");
   
    /* Update date_input plugin so that MM/DD/YYYY format is used. */
    $.extend(DateInput.DEFAULT_OPTS, {
        stringToDate: function(string) {
            var matches;
            if(matches = string.match(/^(\d{2,2})\/(\d{2,2})\/(\d{4,4})$/)) {
                return new Date(matches[3], matches[1] - 1, matches[2]);
            } else {
                return null;
            }
        },
        dateToString: function(date) {
            var month = (date.getMonth() + 1).toString();
            var dom = date.getDate().toString();
            if(month.length == 1) month = "0" + month;
            if(dom.length == 1) dom = "0" + dom;
            return month + "/" + dom + "/" + date.getFullYear();
        }
    });

    /* Attach datepickers to fields! */
    $('input.datepicker').date_input();

    console.log("ready() done");
});

