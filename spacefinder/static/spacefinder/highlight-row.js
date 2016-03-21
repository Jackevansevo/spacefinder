$(document).ready(function() {
    var stateColors = {
        "Busy": "danger",
        "Quite Busy": "warning",
        "Average": "active",
        "Quite Empty": "info",
        "Empty": "success"
    };

    // Highlight each study space entry with it's corresponding busyness colour
    $('#studySpaceTable table tr td:nth-child(3)').each(function () {
        $(this).closest('tr').addClass(stateColors[$(this).text()])
    });
});
