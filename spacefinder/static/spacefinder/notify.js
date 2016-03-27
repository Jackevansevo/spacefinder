$(document).ready(function () {

    notifications.forEach(function(notification) {
        $.notify(notification, {
            placement: {
                from: "bottom",
                align: "right"
            },
            type: "success"
        });
    });

});
