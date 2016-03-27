$(document).ready(function() {

    emojis = ["#busy-emoji", "#quite-busy-emoji", "#average-emoji", "#quite-empty-emoji", "#empty-emoji"];

    // Shade all the emojis
    $(".emoji").css("opacity", "0.2");

    // Unshade the current slider position
    $((emojis[$("#slider").val()-1])).css("opacity", "1");

    // Get slider position
    var sliderPos = $("#slider").val();

    // Update the slider whenever the emojis are changed
    $("#slider").on("input change", function() {
        var newPos = $("#slider").val();

        // Only animate emojis if slider position is different
        if(sliderPos != newPos) {

            var index = newPos-1;

            // Stop any other still running animations
            for(var i=0; i < emojis.length; i ++) {
                if(i != index) {
                    $(emojis[index]).velocity("stop");
                }
            }

            // Shade all the emojis
            $(".emoji").css("opacity", "0.2");

            // Animate the selected emoji
            $(emojis[index]).velocity('callout.bounce');

            // Unshade the selected one
            $((emojis[index])).css("opacity", "1");
        }
        sliderPos = $("#slider").val();
    });
});
