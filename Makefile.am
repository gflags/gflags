## Process this file with automake to produce Makefile.in

# Make sure that when we re-make ./configure, we get the macros we need
ACLOCAL_AMFLAGS = -I m4

# This is so we can #include <gflags/foo>
AM_CPPFLAGS = -I$(top_srcdir)/src

# This is mostly based on configure options
AM_CXXFLAGS =

# These are good warnings to turn on by default,
if GCC
AM_CXXFLAGS += -Wall -Wwrite-strings -Woverloaded-virtual -Wno-sign-compare
endif

# The -no-undefined flag allows libtool to generate shared libraries for
# Cygwin and MinGW.  LIBSTDCXX_LA_LINKER_FLAG is used to fix a Solaris bug.
AM_LDFLAGS = -no-undefined $(LIBSTDCXX_LA_LINKER_FLAG)

gflagsincludedir = $(includedir)/gflags
## The .h files you want to install (that is, .h files that people
## who install this package can include in their own applications.)
gflagsinclude_HEADERS = src/gflags/gflags.h src/gflags/gflags_completions.h

# This is for backwards compatibility only.
googleincludedir = $(includedir)/google
googleinclude_HEADERS = src/google/gflags.h src/google/gflags_completions.h

bin_SCRIPTS = src/gflags_completions.sh

docdir = $(prefix)/share/doc/$(PACKAGE)-$(VERSION)
## This is for HTML and other documentation you want to install.
## Add your documentation files (in doc/) in addition to these
## top-level boilerplate files.  Also add a TODO file if you have one.
dist_doc_DATA = AUTHORS COPYING ChangeLog INSTALL NEWS README \
	doc/designstyle.css doc/gflags.html

## The libraries (.so's) you want to install
lib_LTLIBRARIES =

## unittests you want to run when people type 'make check'.
## TESTS is for binary unittests, check_SCRIPTS for script-based unittests.
## TESTS_ENVIRONMENT sets environment variables for when you run unittest,
## but it only seems to take effect for *binary* unittests (argh!)
TESTS =
TESTS_ENVIRONMENT = SRCDIR="$(top_srcdir)"
check_SCRIPTS =
# Every time you add a unittest to check_SCRIPTS, add it here too
noinst_SCRIPTS =
# Used for auto-generated source files
CLEANFILES =

## vvvv RULES TO MAKE THE LIBRARIES, BINARIES, AND UNITTESTS

GFLAGS_SOURCES = $(gflagsinclude_HEADERS) src/config.h src/mutex.h \
                 src/gflags.cc src/gflags_reporting.cc \
                 src/gflags_completions.cc

lib_LTLIBRARIES += libgflags.la
libgflags_la_SOURCES = $(GFLAGS_SOURCES)
libgflags_la_CXXFLAGS = $(PTHREAD_CFLAGS) -DNDEBUG
libgflags_la_LDFLAGS = $(PTHREAD_CFLAGS)
libgflags_la_LIBADD = $(PTHREAD_LIBS)

lib_LTLIBRARIES += libgflags_nothreads.la
libgflags_nothreads_la_SOURCES = $(GFLAGS_SOURCES)
libgflags_nothreads_la_CXXFLAGS = -DNDEBUG -DNO_THREADS

TESTS += gflags_unittest$(EXEEXT)
gflags_unittest_SOURCES = $(gflagsinclude_HEADERS) src/config.h \
                          src/gflags_unittest.cc
gflags_unittest_CXXFLAGS = $(PTHREAD_CFLAGS)
gflags_unittest_LDFLAGS = $(PTHREAD_CFLAGS)
gflags_unittest_LDADD = libgflags.la

# Also make sure this works when we don't link in pthreads
TESTS += gflags_nothreads_unittest$(EXEEXT)
gflags_nothreads_unittest_SOURCES = $(gflags_unittest_SOURCES)
gflags_nothreads_unittest_LDADD = libgflags_nothreads.la

# We also want to test that things work properly when the file that
# holds main() has a name ending with -main or _main.  To keep the
# Makefile small :-), we test the no-threads version of these.
TESTS += gflags_unittest2$(EXEEXT)
gflags_unittest2_SOURCES = $(gflagsinclude_HEADERS) src/config.h \
                           src/gflags_unittest-main.cc
gflags_unittest2_LDADD = libgflags_nothreads.la
src/gflags_unittest-main.cc: src/gflags_unittest.cc
	rm -f src/gflags_unittest-main.cc
	cp -p src/gflags_unittest.cc src/gflags_unittest-main.cc
CLEANFILES += src/gflags_unittest-main.cc

TESTS += gflags_unittest3$(EXEEXT)
gflags_unittest3_SOURCES = $(gflagsinclude_HEADERS) src/config.h \
	                   src/gflags_unittest_main.cc
gflags_unittest3_LDADD = libgflags_nothreads.la
src/gflags_unittest_main.cc: src/gflags_unittest.cc
	rm -f src/gflags_unittest_main.cc
	cp -p src/gflags_unittest.cc src/gflags_unittest_main.cc
CLEANFILES += src/gflags_unittest_main.cc

# Some buggy sh's ignore "" instead of treating it as a positional
# parameter.  Since we use "" in this script, we prefer bash if we
# can.  If there's no bash, we fall back to sh.
check_SCRIPTS += gflags_unittest_sh
noinst_SCRIPTS += src/gflags_unittest.sh
dist_noinst_DATA = src/gflags_unittest_flagfile
gflags_unittest_sh: gflags_unittest$(EXEEXT) \
                    gflags_unittest2$(EXEEXT) \
                    gflags_unittest3$(EXEEXT)
	bash --version >/dev/null && export SH=bash || export SH=sh; \
	$$SH "$(top_srcdir)/src/gflags_unittest.sh" "$(PWD)/gflags_unittest" \
                                                    "$(top_srcdir)"

# These aren't part of the c++ source, but we want them to be distributed
PYTHON = python/setup.py \
         python/gflags.py \
         python/gflags2man.py \
         python/gflags_unittest.py \
         python/test_module_foo.py \
         python/test_module_bar.py


## ^^^^ END OF RULES TO MAKE THE LIBRARIES, BINARIES, AND UNITTESTS


## This should always include $(TESTS), but may also include other
## binaries that you compile but don't want automatically installed.
noinst_PROGRAMS = $(TESTS)

rpm: dist-gzip packages/rpm.sh packages/rpm/rpm.spec
	@cd packages && ./rpm.sh ${PACKAGE} ${VERSION}

deb: dist-gzip packages/deb.sh packages/deb/*
	@cd packages && ./deb.sh ${PACKAGE} ${VERSION}

libtool: $(LIBTOOL_DEPS)
	$(SHELL) ./config.status --recheck
EXTRA_DIST = packages/rpm.sh packages/rpm/rpm.spec packages/deb.sh packages/deb \
	libtool $(SCRIPTS) $(PYTHON) \
        src/solaris/libstdc++.la
