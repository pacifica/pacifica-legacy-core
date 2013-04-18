test("download request", function() {
	stop();
	if($('.myemsl_download_iframe').length <= 1) {
		var iframe = $('<iframe src="about:blank" id="myemsl_download_iframe">');
		iframe.removeAttr('style').css('display', 'none');
		$('body').append(iframe);
	}
	$('#myemsl_download_iframe').ready(function() {
		ok(this.location.href != 'about:blank', "Passed!");
		start();
	});
	$('#myemsl_download_iframe').attr('src', 'testdownload.php');
});

test("head ajax request", function() {
	stop();
	$.ajax({
		type: "HEAD",
		async: true,
		url: "testheader.php",
		complete: function(response, text) {
			var custom_header = response.getResponseHeader('x-Custom');
			ok(custom_header == "foo", "Passed!");
			start();
		},
		error: function(message, text, response) {
			ok(false, "Something bad happened");
		}
	});
});

test("timeago time", function() {
	$('body').append('<time id="datetimetest" datetime="2011-06-07T12:54:23-07:00">Time</time>');
	$('#datetimetest').hide().timeago();
	ok(true, "Passed");
});

test("timeago abbr", function() {
	$('body').append('<abbr id="datetimetest" title="2011-06-07T12:54:23-07:00">Time</abbr>');
	$('#datetimetest').hide().timeago();
	ok(true, "Passed");
});
