MAINTAINERCLEANFILES = Makefile.in build

EXTRA_DIST = \
myemsl/util.py \
myemsl/archive.py \
myemsl/dbconnect/__init__.py \
myemsl/metadata/__init__.py \
myemsl/getconfig/__init__.py \
myemsl/getservices/__init__.py \
myemsl/getstatusremote/__init__.py \
myemsl/getunixuser/__init__.py \
myemsl/uploader/__init__.py \
myemsl/getuserremote/__init__.py \
myemsl/eushandoff/__init__.py \
myemsl/nagiosrmtransremote/__init__.py \
myemsl/eus2login/__init__.py \
myemsl/getpermission/__init__.py \
myemsl/permission/__init__.py \
myemsl/pam/__init__.py \
myemsl/__init__.py \
myemsl/logging.py \
myemsl/catchall.py \
myemsl/id2filename.py \
myemsl/cart/__init__.py \
myemsl/callcurl/__init__.py \
myemsl/brand/__init__.py \
myemsl/token/__init__.py \
myemsl/token/uuid.py \
myemsl/token/sign.py \
myemsl/token/verify.py \
myemsl/token/rfc3339enc.py \
myemsl/token/minify_json.py \
myemsl/token/rfc3339parse.py \
myemsl/auth/__init__.py \
myemsl/auth/modpython/__init__.py \
myemsl/auth/modpython/item/__init__.py \
myemsl/loadkeytab/__init__.py \
myemsl/userrewritehandler/__init__.py \
myemsl/authenhandler/__init__.py \
myemsl/authenhandler/myemslcore.py \
myemsl/authenhandler/storage.py \
myemsl/getfileremote/__init__.py \
myemsl/websessionremote/__init__.py \
myemsl/eus2myemsl/__init__.py \
myemsl/euslogin/__init__.py \
myemsl/bundler/__init__.py \
myemsl/inoutage/__init__.py \
myemsl/prefixtree/__init__.py \
myemsl/elasticsearch/__init__.py \
myemsl/elasticsearch/schema.py \
myemsl/elasticsearch/jsonentry.py \
myemsl/elasticsearch/getalias.py \
myemsl/elasticsearch/createalias.py \
myemsl/elasticsearch/createindex.py \
myemsl/elasticsearch/deleteindex.py \
myemsl/elasticsearch/createuserfilter.py \
myemsl/elasticsearch/jsondumper.py \
myemsl/elasticsearch/rfc3339.py \
myemsl/elasticsearch/bulkaction.py \
myemsl/elasticsearch/unitgen.py \
myemsl/elasticsearch/metadata/__init__.py \
myemsl/elasticsearch/metadata/emsl_base.py \
myemsl/elasticsearch/metadata/emsl_dms.py \
myemsl/authzpersondir/cart.py \
myemsl/authzpersondir/stage.py \
myemsl/authzpersondir/__init__.py \
myemsl/ingest/__init__.py \
myemsl/service/__init__.py \
myemsl/service/qrs/__init__.py \
myemsl/service/auth/__init__.py \
myemsl/service/cart2/__init__.py \
myemsl/service/notify/__init__.py \
myemsl/service/outage/__init__.py \
myemsl/service/dmspath/__init__.py \
myemsl/service/getuser/__init__.py \
myemsl/service/itemauth/__init__.py \
myemsl/service/iteminfo/__init__.py \
myemsl/service/predicate/__init__.py \
myemsl/service/personinfo/__init__.py \
myemsl/service/qrshistory/__init__.py \
myemsl/service/queryengine/__init__.py \
myemsl/service/transaction/__init__.py \
myemsl/service/elasticsearch/__init__.py \
myemsl/service/nagiosrmtrans/__init__.py \
myemsl/service/reprocess/__init__.py \
myemsl/service/sstp/finish.py \
myemsl/service/sstp/status.py \
myemsl/service/sstp/preallocate.py \
myemsl/service/itemserverposix/__init__.py \
myemsl/service/notification/__init__.py \
myemsl/service/admin/__init__.py \
myemsl/service/admin/switchuser/__init__.py \
myemsl/handler/__init__.py \
myemsl/handler/401/__init__.py \
myemsl/handler/qrs/__init__.py \
myemsl/handler/auth/__init__.py \
myemsl/handler/cart2/__init__.py \
myemsl/handler/query/__init__.py \
myemsl/handler/logout/__init__.py \
myemsl/handler/notify/__init__.py \
myemsl/handler/outage/__init__.py \
myemsl/handler/dmspath/__init__.py \
myemsl/handler/getuser/__init__.py \
myemsl/handler/itemauth/__init__.py \
myemsl/handler/iteminfo/__init__.py \
myemsl/handler/predicate/__init__.py \
myemsl/handler/queryraw/__init__.py \
myemsl/handler/eushandoff/__init__.py \
myemsl/handler/personinfo/__init__.py \
myemsl/handler/qrshistory/__init__.py \
myemsl/handler/transaction/__init__.py \
myemsl/handler/elasticsearch/__init__.py \
myemsl/handler/nagiosrmtrans/__init__.py \
myemsl/handler/reprocess/__init__.py \
myemsl/handler/personinforaw/__init__.py \
myemsl/handler/sstp/finish/__init__.py \
myemsl/handler/sstp/preallocate/__init__.py \
myemsl/handler/notification/__init__.py \
myemsl/handler/admin/__init__.py \
myemsl/handler/admin/switchuser/__init__.py \
scripts/myemslupload \
scripts/myemslbundler \
scripts/myemsl_unitsearch_import \
scripts/myemsl_getunixuser

all-local:
	export MODSRCDIR=`bash -c 'cd "$(srcdir)" 2>/dev/null && pwd || echo "$(srcdir)"'`; if [ $$MODSRCDIR != `pwd` ]; then echo Going to do: cp -a $$MODSRCDIR `pwd`; mkdir -p myemsl; cp -a $$MODSRCDIR/myemsl/* myemsl; chmod 700 myemsl; touch myemsl/.distclean; chmod 600 myemsl/*; fi;
	$(PYTHON) ./setup.py build $(SETUP_ARGS)

install-am: all-local
	$(PYTHON) ./setup.py install --prefix $(DESTDIR)/${prefix}

maintainer-clean-local: clean-local
	$(PYTHON) ./setup.py clean $(SETUP_ARGS)
	$(RM) -rf $(MAINTAINERCLEANFILES)

uninstall-local: all-local
	export MODULEPATH=`$(PYTHON) -c 'import sys; import re; reg="%s/lib[0-9]*/python%i.%i/site-packages$$" %(sys.prefix, sys.version_info[0], sys.version_info[1]); rec = re.compile(reg); print filter(lambda x: rec.match(x) != None, sys.path)[0][len(sys.prefix):]'`; if [ -d "$(DESTDIR)/$(prefix)/$$MODULEPATH/myemsl" ]; then rm -rf "$(DESTDIR)/$(prefix)/$$MODULEPATH/myemsl"; fi

clean-local:
	$(PYTHON) ./setup.py clean
	$(RM) -rf build

distclean-local: clean-local
	@test -f myemsl/.distclean && rm -rf myemsl


