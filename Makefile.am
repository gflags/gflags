## This is a boilerplate file for Google opensource projects.
## To make it useful, replace <<TEXT>> with actual text for your project.
## Also, look at comments with "## double hashes" to see if any are worth
## uncommenting or modifying.

## Process this file with automake to produce Makefile.in

# Make sure that when we re-make ./configure, we get the macros we need
ACLOCAL_AMFLAGS = -I m4

# This is so we can #include <google/foo>
AM_CPPFLAGS = -I$(top_srcdir)/src

# This is mostly based on configure options
AM_CXXFLAGS =

# These are good warnings to turn on by default,
if GCC
AM_CXXFLAGS += -Wall -Wwrite-strings -Woverloaded-virtual -Wno-sign-compare
endif

googleincludedir = $(includedir)/google
## The .h files you want to install (that is, .h files that people
## who install this package can include in their own applications.)
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

lib_LTLIBRARIES += libgflags.la
libgflags_la_SOURCES = $(googleinclude_HEADERS) src/config.h \
                       src/gflags.cc src/gflags_reporting.cc \
                       src/gflags_completions.cc
libgflags_la_CXXFLAGS = $(PTHREAD_CFLAGS) -DNDEBUG
libgflags_la_LDFLAGS = $(PTHREAD_CFLAGS)
libgflags_la_LIBADD = $(PTHREAD_LIBS)

TESTS += gflags_unittest
gflags_unittest_SOURCES = $(googleinclude_HEADERS) src/config.h \
                          src/gflags_unittest.cc
gflags_unittest_CXXFLAGS = $(PTHREAD_CFLAGS)
gflags_unittest_LDFLAGS = $(PTHREAD_CFLAGS)
gflags_unittest_LDADD = libgflags.la $(PTHREAD_LIBS)

# Also make sure this works when we don't link in pthreads
TESTS += gflags_nothreads_unittest
gflags_nothreads_unittest_SOURCES = $(gflags_unittest_SOURCES)
gflags_nothreads_unittest_LDADD = libgflags.la

# We also want to test that things work properly when the file that
# holds main() has a name ending with -main or _main.  To keep the
# Makefile small :-), we test the no-threads version of these.
TESTS += gflags_unittest2
gflags_unittest2_SOURCES = $(googleinclude_HEADERS) src/config.h \
                           src/gflags_unittest-main.cc
gflags_unittest2_LDADD = libgflags.la
src/gflags_unittest-main.cc: src/gflags_unittest.cc
	rm -f src/gflags_unittest-main.cc
	cp -p src/gflags_unittest.cc src/gflags_unittest-main.cc
CLEANFILES += src/gflags_unittest-main.cc

TESTS += gflags_unittest3
gflags_unittest3_SOURCES = $(googleinclude_HEADERS) src/config.h \
	                   src/gflags_unittest_main.cc
gflags_unittest3_LDADD = libgflags.la
src/gflags_unittest_main.cc: src/gflags_unittest.cc
	rm -f src/gflags_unittest_main.cc
	cp -p src/gflags_unittest.cc src/gflags_unittest_main.cc
CLEANFILES += src/gflags_unittest_main.cc


check_SCRIPTS += gflags_unittest_sh
noinst_SCRIPTS += src/gflags_unittest.sh
dist_noinst_DATA = $(top_srcdir)/src/gflags_unittest_flagfile
gflags_unittest_sh: gflags_unittest gflags_unittest2 gflags_unittest3
	$(top_srcdir)/src/gflags_unittest.sh $(PWD)/$< $(top_srcdir)

# These aren't part of the c++ source, but we want them to be distributed
PYTHON = python/setup.py \
         python/gflags.py \
         python/gflags2man.py \
         python/gflags_unittest.py


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
	libtool $(SCRIPTS) $(PYTHON)
