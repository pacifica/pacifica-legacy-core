#This is kind-of an ungly hack... Revisit later.

SUBDIRS = elasticsearch

apidir = $(pkgmyemslwebapidir)/1
api_DATA = myemsl-widgets.js \
	myemsl-widgets.min.js \
	myemsl-widgets-standalone.js \
	myemsl-widgets-standalone.min.js \
	myemsl-search-pager-helper.js \
	myemsl-search-pager.js \
	myemsl-widgets.css \
	myemsl-widgets-main.js \
	/usr/lib/pacifica/builddeps/jquery.timeago.js \
	builddir/jquery.ui.selectmenu.js \
	/usr/lib/pacifica/builddeps/modernizr.js \
	/usr/lib/pacifica/builddeps/JSON-js/json2.js \
	/usr/lib/pacifica/builddeps/jquery.min.js \
	/usr/lib/pacifica/builddeps/jquery-ui/js/jquery-ui.min.js \
	/usr/lib/pacifica/builddeps/jquery-jtemplates.js \
	builddir/jaysun.js \
	/usr/lib/pacifica/builddeps/r.js/require.js

EXTRA_DIST = myemsl-widgets-base.js \
	jqueryheader \
	jqueryuiheader \
	jqueryfooter \
	app.build.js \
	myemsl-search-pager-helper.js \
	myemsl-search-pager.js \
	myemsl-widgets-search.css \
	myemsl-widgets-main.js

myemsl-widgets.css: myemsl-widgets-search.css /usr/lib/pacifica/builddeps/jquery.ui.selectmenu.css
	cat /usr/lib/pacifica/builddeps/jquery.ui.selectmenu.css myemsl-widgets-search.css > myemsl-widgets.css

clean-local:
	rm -f myemsl-widgets.js myemsl-widgets.min.js myemsl-widgets-standalone.js myemsl-widgets-standalone.min.js
	rm -rf builddir
	rm -rf tmp

install-data-local:
	$(mkdir_p) "$(DESTDIR)$(pkgmyemslwebapidir)/1/css/ui-lightness"
	here=`pwd`; cd "$(DESTDIR)$(pkgmyemslwebapidir)/1/css/ui-lightness" && tar -cf - -C "/usr/lib/pacifica/builddeps/jquery-ui/css/ui-lightness" . | tar -xf -

builddir/jaysun.js: builddir /usr/lib/pacifica/builddeps/jaysun.js
	sed 's/\.live(/.on(/g' /usr/lib/pacifica/builddeps/jaysun.js > builddir/jaysun.js

builddir/jquery.ui.selectmenu.js: builddir

#Make all of the dependencies that are not AMD aware, so.
builddir:
	mkdir builddir
	cat /usr/lib/pacifica/builddeps/jquery.min.js > builddir/jquery.js
	(cat jqueryheader /usr/lib/pacifica/builddeps/jquery-ui/js/jquery-ui.min.js jqueryfooter) > builddir/jquery.ui.js
	(cat jqueryheader "../../static/1/label_over.js" jqueryfooter) > builddir/label_over.js
	(cat jqueryuiheader /usr/lib/pacifica/builddeps/jquery.formwizard/js/jquery.validate.js jqueryfooter) > builddir/jquery.validate.js
	(cat jqueryuiheader /usr/lib/pacifica/builddeps/jquery.formwizard/js/jquery.form.js jqueryfooter) > builddir/jquery.form.js
	(cat jqueryuiheader /usr/lib/pacifica/builddeps/jquery.formwizard/js/jquery.form.wizard.js jqueryfooter) > builddir/jquery.form.wizard.js
	(cat jqueryuiheader /usr/lib/pacifica/builddeps/jquery.formwizard/js/bbq.js jqueryfooter) > builddir/bbq.js
	(cat jqueryuiheader /usr/lib/pacifica/builddeps/jQuery-Timepicker-Addon/jquery-ui-timepicker-addon.js jqueryfooter) > builddir/jquery.ui.timepicker-addon.js
	(cat jqueryuiheader /usr/lib/pacifica/builddeps/jQuery-Timepicker-Addon/jquery-ui-sliderAccess.js jqueryfooter) > builddir/jquery.ui.sliderAccess.js
	(cat jqueryuiheader /usr/lib/pacifica/builddeps/jquery.ui.selectmenu.js jqueryfooter) > builddir/jquery.ui.selectmenu.js

myemsl-widgets.js: myemsl-widgets-base.js builddir
	java -classpath /usr/lib/pacifica/builddeps/r.js/lib/rhino/js.jar:/usr/lib/pacifica/builddeps/r.js/lib/closure/compiler.jar org.mozilla.javascript.tools.shell.Main /usr/lib/pacifica/builddeps/r.js/dist/r.js -o app.build.js
	cat tmp/myemsl-widgets-base.js > myemsl-widgets.js

myemsl-widgets.min.js: myemsl-widgets.js
	cat myemsl-widgets.js > myemsl-widgets.min.js

#The end result are two javascript files that completely containerize and isolate the code.
myemsl-widgets-standalone.js: myemsl-widgets.js
	(echo '(function() {'; cat tmp/almond.js myemsl-widgets.js; echo '; var jQuery = window.jQuery.noConflict(true); window.myemslRequire = require;}());') > myemsl-widgets-standalone.js

myemsl-widgets-standalone.min.js: myemsl-widgets-standalone.js
	cat myemsl-widgets-standalone.js > myemsl-widgets-standalone.min.js
