$(document).ready(function () {
    var stateColors = {
        "Busy": "#EBCCCC",
        "Quite Busy": "#FAF2CC",
        "Average": "#E8E8E8",
        "Quite Empty": "#C4E3F3",
        "Empty": "#D0E9C6"
    };

    $("body").css("background", stateColors[$("#status").text()]);
});
