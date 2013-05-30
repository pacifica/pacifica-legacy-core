if WITH_RMDS
MAYBE_RMDS = ssl/rmds.conf
endif

EXTRA_DIST = eushandoff.conf.in getuser.conf.in \
             ingest.conf.in iteminfo.conf.in nagiosrmtrans.conf.in \
             outage.conf.in query.conf.in query-raw.conf.in \
             query-wsgi.conf.in status.conf.in testauth.conf.in \
             auth.conf.in logout.conf.in notify.conf.in \
             transaction.conf.in error_nopersonid.conf.in 401.conf.in \
             sampleingest.conf.in client.conf.in personinfo.conf.in \
             personinforaw.conf.in cart.conf.in services.conf.in \
             item.conf.in preferences.conf.in query-triple.conf.in \
             elasticsearch.conf.in simple-search.conf.in \
             proposal-finder.conf.in static.conf.in api.conf.in \
             predicate.conf.in test.conf.in elasticsearch-proxy.conf.in \
             cart-local.conf.in cart-proxy.conf.in cart-proxy-ssl.conf.in \
             dmspath.conf.in admin.conf.in rmds.conf.in rmds2.conf.in

pkgmyemslweb_DATA = web/ingest.conf web/query.conf web/testauth.conf \
                    web/iteminfo.conf web/status.conf web/outage.conf \
                    web/auth.conf web/logout.conf web/error_nopersonid.conf \
                    web/401.conf web/sampleingest.conf web/client.conf \
                    web/personinfo.conf web/cart.conf web/services.conf \
                    web/item.conf web/preferences.conf \
                    web/elasticsearch.conf web/simple-search.conf \
                    web/proposal-finder.conf web/static.conf web/api.conf \
                    web/predicate.conf web/test.conf web/admin.conf \
                    web/elasticsearch-proxy.conf web/cart-local.conf \
                    web/cart-proxy.conf web/dmspath.conf


pkgmyemslssl_DATA = ssl/ingest.conf ssl/query.conf ssl/query-raw.conf \
                    ssl/testauth.conf ssl/iteminfo.conf ssl/getuser.conf \
                    ssl/status.conf ssl/eushandoff.conf $(MAYBE_RMDS) \
                    ssl/nagiosrmtrans.conf ssl/outage.conf ssl/auth.conf \
                    ssl/logout.conf ssl/notify.conf ssl/transaction.conf \
                    ssl/error_nopersonid.conf ssl/sampleingest.conf \
                    ssl/personinfo.conf ssl/personinforaw.conf \
                    ssl/cart.conf ssl/services.conf ssl/item.conf \
                    ssl/preferences.conf ssl/elasticsearch.conf \
                    ssl/simple-search.conf ssl/proposal-finder.conf \
                    ssl/static.conf ssl/api.conf ssl/predicate.conf \
                    ssl/client.conf ssl/test.conf ssl/admin.conf \
                    ssl/elasticsearch-proxy.conf ssl/cart-local.conf \
                    ssl/cart-proxy-ssl.conf ssl/dmspath.conf ssl/rmds2.conf

$(pkgmyemslweb_DATA):
	$(mkdir_p) web
	sed 's:@WEBAUTH@:/etc/myemsl/webauth.conf:g;s:@WEBAUTH_STORAGE@:/usr/lib/myemsl/apache/webauth-storage.conf:g;s:@WEBAUTH_MYEMSL@:/usr/lib/myemsl/apache/webauth-myemsl.conf:g' \
	$(shell basename $(@)).in > ./$(@)

$(pkgmyemslssl_DATA):
	$(mkdir_p) ssl
	sed 's:@WEBAUTH@:/etc/myemsl/webauth-ssl.conf:g;s:@WEBAUTH_STORAGE@:/usr/lib/myemsl/apache/webauth-storage.conf:g;s:@WEBAUTH_MYEMSL@:/usr/lib/myemsl/apache/webauth-myemsl.conf:g' \
	$(shell basename $(@)).in > ./$(@)

clean-generic:
	$(RM) -r ssl web
