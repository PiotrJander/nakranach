$container = $ '#tap-changes'
template = $ '#tap-change-template' 
    .text()

show_changes = (data) ->
    $container.empty()

    for change in data
        change.timestamp = moment change.timestamp 
            .calendar()

        $ Mustache.render template, change 
            .appendTo $container


refresh_changes = () ->
    $.get URLs.tap_changes, show_changes

setInterval refresh_changes, 60000

refresh_changes()