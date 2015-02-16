(function() {
  Mustache.tags = ['[[', ']]'];

  window.Helpers = {
    template: function(name) {
      return $("#" + name + "-template").text();
    },
    show_data: function(data, $container, template, additional_processing) {
      var piece, _i, _len, _results;
      $container.empty();
      additional_processing = additional_processing || function(data) {
        return {};
      };
      _results = [];
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        piece = data[_i];
        additional_processing(piece);
        _results.push($(Mustache.render(template, piece)).appendTo($container));
      }
      return _results;
    }
  };

}).call(this);
