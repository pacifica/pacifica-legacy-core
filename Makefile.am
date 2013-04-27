ACLOCAL_AMFLAGS = -I m4

SUBDIRS = src conf test docs

dist-hook:
	$(top_srcdir)/svnver.sh $(top_srcdir) > $(distdir)/svnver.txt
	$(top_srcdir)/svnbranch.sh $(top_srcdir) > $(distdir)/svnbranch.txt

EXTRA_DIST = myemsl.spec svnver.sh svnbranch.sh

DEV=1
REVISION=1
OTHERREVISION=1

rpm: dist
	mkdir -p packages
	rm -rf packages
	mkdir -p packages/bin
	mkdir -p packages/src
	if [ "x${DEV}" != "x1" ]; \
	then \
		rpmbuild -ta @PACKAGE_NAME@-@VERSION@.tar.gz --define '_rpmdir '`pwd`'/packages/bin' --define '_srcrpmdir '`pwd`'/packages/src' --define "LOCALREVISION ${REVISION}" --define ' rhel 5'; \
	else \
		LOCALREVISION="`git rev-list HEAD | wc -l`"; \
		if [ $$LOCALREVISION -lt ${OTHERREVISION} ]; then \
			LOCALREVISION=${OTHERREVISION}; \
		fi;\
		LOCALREVISION="git$$LOCALREVISION"; \
		echo revision="$$LOCALREVISION"; \
		rpmbuild -ta @PACKAGE_NAME@-@VERSION@.tar.gz --define '_rpmdir '`pwd`'/packages/bin' --define '_srcrpmdir '`pwd`'/packages/src' --define "LOCALREVISION `echo $$LOCALREVISION`" --define ' rhel 5'; \
	fi

rpms: rpm

MOCKDIST=fedora-18-x86_64
MOCK=/usr/bin/mock

mock: dist
	rm -rf packages/"$(MOCKDIST)" || true
	mkdir -p packages/"$(MOCKDIST)"/srpms
	mkdir -p packages/"$(MOCKDIST)"/bin
	LOCALREVISION="`git rev-list HEAD | wc -l`"; \
	if [ $$LOCALREVISION -lt ${OTHERREVISION} ]; then \
		LOCALREVISION=${OTHERREVISION}; \
	fi; \
	LOCALREVISION="git$$LOCALREVISION"; \
	echo revision="$$LOCALREVISION"; \
	$(MOCK) -r "$(MOCKDIST)" --buildsrpm --spec myemsl.spec --sources "`pwd`" --define "LOCALREVISION `echo $$LOCALREVISION`"; \
	mv "/var/lib/mock/$(MOCKDIST)/result/"*.src.rpm packages/"$(MOCKDIST)"/srpms/; \
	$(MOCK) -r "$(MOCKDIST)" --result "$(CURDIR)"/packages/"$(MOCKDIST)"/bin --define "LOCALREVISION `echo $$LOCALREVISION`" "$(CURDIR)"/packages/"$(MOCKDIST)"/srpms/*.src.rpm; \
if [ $$? -ne 0 ]; then \
	cat "$(CURDIR)"/packages/"$(MOCKDIST)"/bin/build.log; \
fi
