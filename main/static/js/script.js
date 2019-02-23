$(document).ready(function () {
    $(function () {
        $('.language-switcher').click(function (e) {
            $('#lang-form').submit();
        });
    });

    $(function () {
        // Create a new instance of Slidebars
        var controller = new slidebars();
        // Initialize Slidebars
        controller.init();

        $('.js-toggle-slidebar').on('click', function (event) {
            event.stopPropagation();
            controller.toggle('menu-slidebar');
        });

        $(controller.events).on('opened', function () {
            $('[canvas="container"]').addClass('js-close-slidebar');
        });

        $(controller.events).on('closed', function () {
            $('[canvas="container"]').removeClass('js-close-slidebar');
        });

        $('body').on('click', '.js-close-slidebar', function (event) {
            event.stopPropagation();
            controller.close('menu-slidebar');
        });
    });
});