function validateSplit(input) {
    if (!input.match(/^[\d\+\/\*\-\(\)\. ]*$/)) {
        return Number.NaN;
    }
    if (input.match(/([\+\/\*\-])\1/)) {
        return Number.NaN;
    }
    try {
        v = eval(input);
    } catch (err) {
        return Number.NaN;
    }
    if (v == null) {
        return 0;
    }
    return v;
}

function calcSplit() {
    amount = document.getElementById("amount").value;
    total = 0;
        var values = new Array();
    textvals = document.getElementsByClassName("share-text");
    for (i=0; i<textvals.length; i++) {
        v = validateSplit(textvals[i].value);
        if (!isNaN(v)) {
            total += v;
        }
        values[i] = v;
    }
    for (i=0; i<textvals.length; i++) {
        id = textvals[i].id+'-calc';
        val = (amount*values[i]/total).toFixed(2);
        document.getElementById(id).innerHTML = val;
    }
}

window.onload=calcSplit;
