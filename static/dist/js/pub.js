(function() {
  var $change_container, $tap_container, change_template, refresh_changes, refresh_taps, tap_template;

  $tap_container = $('#taps');

  tap_template = Helpers.template('tap');

  refresh_taps = function() {
    return $.get(URLs.taps, function(data) {
      return Helpers.show_data(data, $tap_container, tap_template);
    });
  };

  refresh_taps();

  $change_container = $('#changes');

  change_template = Helpers.template('change');

  refresh_changes = function() {
    return $.get(URLs.changes, function(data) {
      return Helpers.show_data(data, $change_container, change_template, function(data) {
        return data.timestamp = moment(data.timestamp).calendar();
      });
    });
  };

  refresh_changes();

  setInterval(function() {
    refresh_taps();
    return refresh_changes();
  }, 60000);

}).call(this);
