({
	baseUrl: "./",
	dir: "tmp",
	optimize: "none",
//	optimize: "closure",
//	wrap: true,
	paths: {
		"jaysun": "builddir/jaysun",
		"JSON": "/usr/lib/pacifica/builddeps/JSON-js/json2", //FIXME make this conditional.
		"myemsl-widgets": "myemsl-widgets-base",
		"jquery": "builddir/jquery",
		"jquery.ui": "builddir/jquery.ui",

		"almond": "/usr/lib/pacifica/builddeps/almond",
		"myemsl.generic-finder": "elasticsearch/generic-finder",
		"myemsl.generic-input-plus-finder": "elasticsearch/generic-input-plus-finder",
		"myemsl.search-pager-helper": "myemsl-search-pager-helper",
		"myemsl.search-pager": "myemsl-search-pager",
//FIXME
		"myemsl.generic-predicate-input": "elasticsearch/generic-predicate-input",
		"myemsl.generic-local-predicate-wizard": "elasticsearch/generic-local-predicate-wizard",
//FIXME

		"label_over": "builddir/label_over",
		"qtip2": "/usr/lib/pacifica/builddeps/qTip2/dist/jquery.qtip",
		"jquery.form": "builddir/jquery.form",
		"jquery.validate": "builddir/jquery.validate",
		"bbq": "builddir/bbq",
		"jquery.timeago": "/usr/lib/pacifica/builddeps/jquery.timeago",
		"jquery.ui.selectmenu": "builddir/jquery.ui.selectmenu",
		"jquery.form.wizard": "builddir/jquery.form.wizard",
		"jquery.ui.sliderAccess": "builddir/jquery.ui.sliderAccess",
		"jquery.ui.timepicker-addon": "builddir/jquery.ui.timepicker-addon"
	},
	modules: [
		{
			name: "almond"
		},
		{
			name: "myemsl-widgets",
			insertRequire: [
				"myemsl-widgets"
			]
		}/*,
		{
			name: "myemsl-widgets-deps",
			exclude: ["jquery"]
		}*/
	],
	include: [
		"myemsl-widgets"
	],
	insertRequire: [
		"myemsl-widgets"
	]
})

