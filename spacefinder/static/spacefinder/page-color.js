$(document).ready(function () {
    var stateColors = {
        "Busy": "#EBCCCC",
        "Quite Busy": "#FAF2CC",
        "Average": "#E8E8E8",
        "Quite Empty": "#C4E3F3",
        "Empty": "#72BF7B"
    };

    $("body").css("background", stateColors[$("#status").text()]);
});
