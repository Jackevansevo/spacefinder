$(document).ready(function() {

    // Make the registration form appear
    $("#registerModal").on('show.bs.modal', function () {
        $('.modal-dialog').velocity('transition.expandIn');
        // Make the deparmtnet dropdown the same colour as the rest of the form
        $('#LoginSelectDepartmentDropDown').css("color", "#999");
        setTimeout(function (){
            $('#RegisterUsername').focus();
        }, 200);
    });

    // Keep popup dialogs on mouse house and close when the mouse leaves
    $('.popoverButton').on("mouseenter", function (e) {
        $(this).popover("show");
        $(this).siblings(".popover").on("mouseleave", function () {
            $(this).popover('hide');
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide");
            }
        }, 100);
    });

    // Popover dialog constructor
    var popoverDialog = function(content) {
        return {
            html: true,
            trigger: 'manual',
            placement: 'bottom',
            content: content
        };
    };

    // Show the login popup dialog
    var loginDialog = popoverDialog($("#loginPopup").html());
    $('#loginButton').popover(loginDialog).on('mouseenter', function() {
        $('#LoginUsername').focus();
    }).on('mouseleave', function() {
        $('#LoginUsername').blur();
    });

    // Show the user profile popup dialog
    var profileDialog = popoverDialog($("#profilePopup").html());
    $('#profileButton').popover(profileDialog);

});
