$(document).ready(function () {

    console.log(message);
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
