$('span.nav-btn').click(function() {
	/* Act on the event */
	$('ul.nav').slidetoggle();
});

$(window).resize(function() {
	/* Act on the event */
	if( $(window).width()>1291){
		$('ul.nav').removeAttr('style');
	}
});