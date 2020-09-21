//   From Bulma Documentation: https://bulma.io/documentation/elements/notification/
document.addEventListener('DOMContentLoaded', () => {
    // Select all the relevant notification classes
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {

        let $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });

        // remove notification after a few seconds
        setTimeout(function () {
            $notification.parentNode.removeChild($notification);
        }, 3000);

    });

    // Show mobile menu on click
    $(".navbar-burger").click(function () {
        $(".navbar-burger").toggleClass("is-active");
        $("#navbar-menu").toggleClass("is-active");
        //fix the body to stop scrolling when in menu
        // src:https://stackoverflow.com/questions/27230955/
        // how-to-disable-scrolling-in-the-background-when-the-mobile-menu-is-open
        $('body').toggleClass("fixed-position");
    });


    // Desktop Search Modal
    $("#search-button").click(function () {
        $('#search-modal').addClass("is-active");
        $("#search-field:text").focus();
    });

    $('.modal-close').click(function () {
        $("#search-modal").removeClass('is-active');
    })

    //dropdowns
    $('#category-btn').click(function () {
        $('#category-menu').toggleClass('is-hidden-mobile');
    })
    $('#genre-btn').click(function () {
        $('#genre-menu').toggleClass('is-hidden-mobile');
    })
    $('#specials-btn').click(function () {
        $('#specials-menu').toggleClass('is-hidden-mobile');
    })
    $('#account-btn').click(function () {
        $('#account-menu').toggleClass('is-hidden-mobile');
    })

// Back to top script
    $('#top-button').click(function () {
        window.scrollTo(0, 0)
    })

    window.onscroll = function () {
        if (pageYOffset >= 200) {
            $('#top-button').removeClass('is-hidden').fadeIn('slow');
        } else {
            $('#top-button').fadeOut('slow');
        }
    };

});