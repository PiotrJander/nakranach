(function() {
  var $container, show_changes;

  $container = $('#tap-changes');

  show_changes = function(data) {
    return console.log(data);
  };

  $.get(URLs.tap_changes, show_changes);

}).call(this);
