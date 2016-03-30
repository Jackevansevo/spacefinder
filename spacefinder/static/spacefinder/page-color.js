$(document).ready(function () {

    // Get the busyness status of the current studyspace
    status = $("#status").text();

    var stateColors = {
        "Empty": "#72BF7B",
        "Quite Empty": "#66C1D5",
        "Average": "#EBEBEB",
        "Quite Busy": "#FFDB7E",
        "Busy": "#DD5864",
    };

    var stateFont = {
        "Empty": "#39603D",
        "Quite Empty": "#4F5B61",
        "Average": "#333333",
        "Quite Busy": "#5C5131",
        "Busy": "#7E383F",
    };


    $("body").css({
        "background": stateColors[status], 
        "color": stateFont[status]
    });

});
