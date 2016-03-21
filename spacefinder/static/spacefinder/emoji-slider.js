$(document).ready(function() {

    emojis = ["#busy-emoji", "#quite-busy-emoji", "#average-emoji", "#quite-empty-emoji", "#empty-emoji"];

    // Shade all the emojis
    $(".emoji").css("opacity", "0.2");

    // Unshade the current slider position
    $((emojis[$("#slider").val()-1])).css("opacity", "1");

    // Get slider position
    sliderPos = $("#slider").val();

    // Update the slider whenever the emojis are changed
    $("#slider").on("input change", function() {
        newPos = $("#slider").val();

        // Only animate emojis if slider position is different
        if(sliderPos != newPos) {

            // Shade all the emojis
            $(".emoji").css("opacity", "0.2");

            // Animate the selected emoji
            $(emojis[$(this).val()-1]).velocity('callout.bounce');

            // Unshade the selected one
            $((emojis[$(this).val()-1])).css("opacity", "1");
        }
        sliderPos = $("#slider").val();
    })
});
