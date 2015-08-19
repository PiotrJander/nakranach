(function() {
  Mustache.tags = ['[[', ']]'];

  window.Helpers = {
    template: function(name) {
      return $("#" + name + "-template").text();
    },
    show_data: function(data, $container, template, additional_processing) {
      var i, len, piece, results;
      $container.empty();
      additional_processing = additional_processing || function(data) {
        return {};
      };
      results = [];
      for (i = 0, len = data.length; i < len; i++) {
        piece = data[i];
        additional_processing(piece);
        results.push($(Mustache.render(template, piece)).appendTo($container));
      }
      return results;
    }
  };

}).call(this);
