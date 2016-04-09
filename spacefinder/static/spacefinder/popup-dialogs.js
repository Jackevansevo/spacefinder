$(document).ready(function() {

    // Popover dialog constructor
    var popoverDialog = function(content) {
        return {
            trigger: 'manual',
            placement: 'bottom',
            html: true,
            content: content,
        };
    };

    // Show the login popup dialog
    var loginDialog = popoverDialog($("#loginPopup").html());
    $('#loginButton').popover(loginDialog);

    // Show the user profile popup dialog
    var profileDialog = popoverDialog($("#profilePopup").html());
    $('#profileButton').popover(profileDialog);

    // Show popover on button clicks
    $('.popoverButton').click(function(e) {
        $(this).popover('toggle');
        e.stopPropagation();
    });

    // Hide popovers when any other html element is clicked
    $('html').click(function(e) {
        if(!$(e.target).parents('.popover-content').length && !$(e.target).hasClass('popover-content')) {
            $('.popoverButton').popover('hide');
        }
    });

    // Show the login popover if errors are present
    if($('#loginErrorMessage').length) {
        $('#loginButton').popover('show');
    }

    // Shows the registration dialogif there are errors present
    if($('#registration-error-msg').length) {
        $('#registerModal').show('show');
        setTimeout(function (){
            $('#RegisterUsername').focus();
        }, 200);
    }

    // Hide the modal on click
    $('button.close').click(function() {
        $('#registerModal').hide();
    });

    // Make the registration form appear
    $("#registerModal").on('show.bs.modal', function () {
        $('.modal-dialog').velocity('transition.bounceDownIn');
        // Make the deparmtnet dropdown the same colour as the rest of the form
        $('#LoginSelectDepartmentDropDown').css("color", "#999");
        setTimeout(function (){
            $('#RegisterUsername').focus();
        }, 200);
    });

});
