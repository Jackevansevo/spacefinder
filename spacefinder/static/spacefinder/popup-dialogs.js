$(document).ready(function() {

    // Make the registration form appear
    $('.modal').each(function(index) {
        $(this).on('show.bs.modal', function (e) {
            $('.modal-dialog').velocity('transition.bounceRightIn');
        })
    })

    // Keep popup dialogs on mouse house and close when the mouse leaves
    $('.popoverButton').on("mouseenter", function () {
        var _this = this;
        $(this).popover("show");
        $(this).siblings(".popover").on("mouseleave", function () {
            $(this).popover('hide');
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide")
            }
        }, 100);
    });

    // Close popup window when users click in areas outside
    $('html').on('click', function(e) {
        if (typeof $(e.target).data('original-title') == 'undefined' &&
            !$(e.target).parents().is('.popover.in')) {
                $('[data-original-title]').popover('hide');
        }
    });

    // Popover dialog constructor
    var popoverDialog = function(_content) {
        return {
            html: true,
            trigger: 'manual',
            placement: 'bottom',
            content: _content
        };
    }

    // Show the login popup dialog
    var loginDialog = popoverDialog($("#loginPopup").html());
    $('#loginButton').popover(loginDialog).on("mouseenter", function () {
        $('#userNameEntry').focus();
    })

    // Show the user profile popup dialog
    var profileDialog = popoverDialog($("#profilePopup").html());
    $('#profileButton').popover(profileDialog)

})
