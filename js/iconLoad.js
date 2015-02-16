(function() {
  $(document).on('ready page:load', function() {
    var gitIcon, homeIcon, mailIcon, smugIcon;
    mailIcon	= new icon("#mailIcon", "../img/mailIcon.svg");
    gitIcon		= new icon("#githubIcon", "../img/githubIcon.svg");
    gitIcon		= new icon("#twitterIcon", "../img/twitterIcon.svg");
    smugIcon	= new icon("#smugIcon", "../img/smugIcon.svg");
    return true;
  });

}).call(this);
