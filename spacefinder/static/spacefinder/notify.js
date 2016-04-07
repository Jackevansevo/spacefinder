$(document).ready(function () {

    if(message.type == "error") {
        message.type = "danger";
    }

    $.notify(message.content, {
        placement: {
            from: "bottom",
            align: "right"
        },
        type:message.type
    });

});
