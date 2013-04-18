require.config({
	paths: {
		"JSON": "/myemsl/api/1/json2", //FIXME make this conditional.
		"jquery.ui": "/myemsl/api/1/jquery-ui.min",
		"jquery.timeago": "/myemsl/api/1/jquery.timeago",
		"jaysun": "/myemsl/api/1/jaysun",
		"label_over": "/myemsl/static/1/label_over",
		"jquery.ui.selectmenu": "/myemsl/api/1/jquery.ui.selectmenu",
		"myemsl.search-pager-helper": "/myemsl/api/1/myemsl-search-pager-helper",
		"myemsl.search-pager": "/myemsl/api/1/myemsl-search-pager",
		"myemsl.generic-finder": "/myemsl/api/1/elasticsearch/generic-finder",
		"myemsl.generic-input-plus-finder": "/myemsl/api/1/elasticsearch/generic-input-plus-finder"
	}
});

define("jquery",
        [],
        function() {
		return $
       }
);
