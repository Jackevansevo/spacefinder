$(document).ready(function () {

    $.notify(message.content, {
        placement: {
            from: "bottom",
            align: "right"
        },
        type:message.type
    });

});
