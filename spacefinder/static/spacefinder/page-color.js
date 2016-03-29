$(document).ready(function () {

    // Get the busyness status of the current studyspace
    status = $("#status").text();

    var stateColors = {
        "Empty": "#72BF7B",
        "Quite Empty": "#D9EDF7",
        "Average": "#EBEBEB",
        "Quite Busy": "#FFDB7E",
        "Busy": "#F06060",
    };

    var stateFont = {
        "Empty": "#39603D",
        "Quite Empty": "#4F5B61",
        "Average": "#333333",
        "Quite Busy": "#5C5131",
        "Busy": "#4E3C3E",
    };

    console.log(stateFont[status]);

    $("body").css({
        "background": stateColors[status], 
        "color": stateFont[status]
    });

});
