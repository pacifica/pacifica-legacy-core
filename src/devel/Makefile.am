sbin_SCRIPTS = myemsl-devel-local myemsl-devel-network-register

reposdir = $(sysconfdir)/yum.repos.d
repos_DATA = myemsl-devel-local.repo

EXTRA_DIST = myemsl-devel-local myemsl-devel-network-register myemsl-devel-local.repo

install-exec-hook:
	mkdir -p $(DESTDIR)/srv/myemsl-devel
