function expandContract() {
    elt = $(this);
    row = elt.parents().find('.expenditure')
    if (row.hasClass('compact')) {
        row.removeClass('compact').addClass('expand');
        elt.attr('src', '/images/expanded.gif');
    }
    else {
        row.removeClass('expand').addClass('compact');
        elt.attr('src', '/images/contracted.gif');
    }
}

function setupExpand() {
    $('.expand_button').click(expandContract)
}

$(document).ready(setupExpand)
