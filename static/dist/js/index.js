(function() {
  var $container, refresh_changes, template;

  $container = $('#tap-changes');

  template = Helpers.template('tap-change');

  refresh_changes = function() {
    return $.get(URLs.tap_changes, function(data) {
      return Helpers.show_data(data, $container, template, function(data) {
        return data.timestamp = moment(data.timestamp).calendar();
      });
    });
  };

  setInterval(refresh_changes, 60000);

  refresh_changes();

}).call(this);
