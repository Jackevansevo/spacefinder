$(document).ready(function () {

    console.log(message);
    $.notify(message.content, {
        placement: {
            from: "bottom",
            align: "right"
        },
        type:message.type
    });

});
