$container = $ '#tap-changes'
template = Helpers.template 'tap-change'

refresh_changes = () ->
    $.get URLs.tap_changes, (data) ->
        Helpers.show_data data, $container, template, (data) ->
            data.timestamp = moment(data.timestamp).calendar()

setInterval refresh_changes, 60000

refresh_changes()