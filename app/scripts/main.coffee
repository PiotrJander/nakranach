Mustache.tags = ['[[', ']]']

window.Helpers = 
    template: (name) ->
        $ "##{name}-template"
            .text()

    show_data: (data, $container, template, additional_processing) ->
        $container.empty()

        additional_processing = additional_processing||(data) -> {}

        for piece in data
            additional_processing piece

            $ Mustache.render template, piece
                .appendTo $container
