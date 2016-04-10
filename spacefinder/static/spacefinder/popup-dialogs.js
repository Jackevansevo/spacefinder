$(document).ready(function() {

    // Shows the registration dialog if there are errors present
    if($('#registration-error-msg').length) {
        $('#registerModal').show('show');
        setTimeout(function (){
            $('#RegisterUsername').focus();
        }, 200);
    }

    // Shows the registration dialog if there are errors present
    if($('#login-error-msg').length) {
        $('#loginModal').show('show');
        setTimeout(function (){
            $('#LoginUsername').focus();
        }, 200);
    }

    // Hide the modal on click
    $('button.close').click(function() {
        $('#registerModal').hide();
        $('#loginModal').hide();
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

    // Make the login form appear
    $("#loginModal").on('show.bs.modal', function () {
        $('.modal-dialog').velocity('transition.bounceDownIn');
        setTimeout(function (){
            $('#LoginUsername').focus();
        }, 200);
    });

});
