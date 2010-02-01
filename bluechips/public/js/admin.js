try {
    console.log("init");
} catch(e) {
    console = { log: function() {} };
}

$(function() {
    console.log("ready()");
   
    /* Attach datepickers to fields! */
    $('input.datepicker').datepicker({
        changeMonth: true,
        changeYear: true,
        duration: '',
        showButtonPanel: true,
    });

    console.log("ready() done");
});

