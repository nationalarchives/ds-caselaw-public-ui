import $ from "jquery";

(function ($) {
    $.fn.manage_filters = function (options) {
        const settings = $.extend({}, $.fn.manage_filters.defaults, options);
        return this.each(() => {

            const $toggle_area = $('.js-results-facets', $(this));

            const $control_container = $('.js-results-control-container', $(this));

            const btn = $('<button>', {
                'class': 'results-search-component__toggle-control',
                'type': 'button',
                'text': settings.expanded_text,
                'click': (e) => {
                    $toggle_area.toggle();

                    const $el = $(e.target);

                    $el.toggleClass('collapsed');

                    $el.text(() => {
                        return $el.text() === settings.collapsed_text ? settings.expanded_text : settings.collapsed_text;
                    })
                }
            });

            if (settings.initially_hidden) {
                btn.trigger('click');
            }

            $control_container.append(btn)
        });
    };

    $.fn.manage_filters.defaults = {
        'collapsed_text': 'Show filter options',
        'expanded_text': 'Hide filter options',
        'initially_hidden': true
    }
}($));


$('.js-results-facets-wrapper').manage_filters();
