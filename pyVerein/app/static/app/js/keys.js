(function($){
    $.fn.nextOnEnter = function() {
        this.keydown(function (event) {
            if (event.which == 13) {
                event.preventDefault();
                var field = event.target;
                if (field.getAttribute('data-next')) {
                    var next = $('#' + field.getAttribute('data-next'));
                    next.focus();
                }
            }
        });
    };  

    $.fn.saveOnTimes = function() {
        this.keydown(function (event) {
            if (event.which == 106) {
                event.preventDefault();
                form.submit();
            }
        });
    };  

    $.fn.exitOnEsc = function(returnUrl) {
        this.keydown(function (event) {
            if (event.which == 27) {
                event.preventDefault();
                window.location = returnUrl
            }
        });
    };  
}(jQuery));
