# taps
$tap_container = $ '#taps'
tap_template = Helpers.template 'tap'

refresh_taps = () ->
    $.get URLs.taps, (data) ->
        Helpers.show_data data, $tap_container, tap_template

refresh_taps()

# changes
$change_container = $ '#changes'
change_template = Helpers.template 'change'

refresh_changes = () ->
    $.get URLs.changes, (data) ->
        Helpers.show_data data, $change_container, change_template, (data) ->
            data.timestamp = moment(data.timestamp).calendar()

refresh_changes()

# set automatic data refresh
setInterval () -> 
        refresh_taps()
        refresh_changes()
    , 60000
