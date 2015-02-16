(function() {
  this.icon = (function() {
    function icon(id, iconFile) {
      var i;
      this.id = id;
      this.iconFile = iconFile;
      this.snapInstance = Snap(this.id);
      i = document.querySelector(this.id);
      i.style.width = 30;
      i.style.height = 30;
      Snap.load(this.iconFile, (function(_this) {
        return function(data) {
          var p1, path1, path2;
          path1 = data.select("#path1").attr({
            fill: '#f1fafb'
          });
          path2 = data.select("#path2").attr({
            fill: '#f1fafb'
          });
          p1 = path1.attr('d');
          _this.snapInstance.append(path1);
          return _this.snapInstance.hover(function() {
            path1.stop();
            return path1.animate({
              d: path2.attr('d'),
              transform: "s.8T"
            }, 1000, mina.bounce);
          }, function() {
            path1.stop();
            return path1.animate({
              d: p1,
              transform: "s1T"
            }, 500, mina.bounce);
          });
        };
      })(this));
    }

    return icon;

  })();

}).call(this);
