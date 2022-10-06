import $ from "jquery";

(function ($) {
    $.fn.manage_filters = function (options) {
        const settings = $.extend({}, $.fn.manage_filters.defaults, options);
        return this.each(() => {
            const $wrapper = $(this);

            const $toggle_area = $(".js-results-facets", $wrapper);

            const $control_container = $(
                ".js-results-control-container",
                $wrapper
            );

            const $filters = $(".js-results-facets-applied-filters", $wrapper);

            window.$ = $;

            const btn = $("<button>", {
                class: "results-search-component__toggle-control collapsed",
                type: "button",
                text:
                    $filters.children().length == 0
                        ? settings.collapsed_text_without_filters
                        : settings.collapsed_text_with_filters,
                click: (e) => {
                    $toggle_area.toggle();

                    const $el = $(e.target);
                    const $filters = $(
                        ".js-results-facets-applied-filters",
                        $wrapper
                    );
                    $el.toggleClass("collapsed");

                    $el.text(() => {
                        if (
                            $el.hasClass("collapsed") &&
                            $filters.children().length == 0
                        ) {
                            return settings.collapsed_text_without_filters;
                        } else if ($el.hasClass("collapsed")) {
                            return settings.collapsed_text_with_filters;
                        } else {
                            return settings.expanded_text;
                        }
                    });
                },
            });

            $control_container.append(btn);
        });
    };

    $.fn.manage_filters.defaults = {
        collapsed_text_with_filters: "Add another filter",
        collapsed_text_without_filters: "Filter by court, date or person",
        expanded_text: "Hide filter options",
    };
})($);

$(".js-results-facets-wrapper").manage_filters();
