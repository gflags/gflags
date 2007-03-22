## This is a boilerplate file for Google opensource projects.
## To make it useful, replace <<TEXT>> with actual text for your project.
## Also, look at comments with "## double hashes" to see if any are worth
## uncommenting or modifying.

## Process this file with automake to produce Makefile.in

# Make sure that when we re-make ./configure, we get the macros we need
ACLOCAL_AMFLAGS = -I `pwd`/../autoconf

# This is so we can #include <google/foo>
AM_CPPFLAGS = -I$(top_srcdir)/src

googleincludedir = $(includedir)/google
## The .h files you want to install (that is, .h files that people
## who install this package can include in their own applications.)
googleinclude_HEADERS = src/google/gflags.h

docdir = $(prefix)/share/doc/$(PACKAGE)-$(VERSION)
## This is for HTML and other documentation you want to install.
## Add your documentation files (in doc/) in addition to these
## top-level boilerplate files.  Also add a TODO file if you have one.
dist_doc_DATA = AUTHORS COPYING ChangeLog INSTALL NEWS README \
	doc/gflags.html

## The libraries (.so's) you want to install
lib_LTLIBRARIES =

## unittests you want to run when people type 'make check'.
## TESTS is for binary unittests, check_SCRIPTS for script-based unittests.
## TESTS_ENVIRONMENT sets environment variables for when you run unittest,
## but it only seems to take effect for *binary* unittests (argh!)
TESTS =
TESTS_ENVIRONMENT =
check_SCRIPTS =
# Every time you add a unittest to check_SCRIPTS, add it here too
noinst_SCRIPTS =


## vvvv RULES TO MAKE THE LIBRARIES, BINARIES, AND UNITTESTS

lib_LTLIBRARIES += libgflags.la
libgflags_la_SOURCES = $(googleinclude_HEADERS) src/config.h \
	src/gflags.cc src/gflags_reporting.cc
libgflags_la_CXXFLAGS = $(PTRHEAD_CFLAGS) -DNDEBUG
libgflags_la_LDFLAGS = $(PTRHEAD_CFLAGS)
libgflags_la_LIBADD = $(PTHREAD_LIBS)

TESTS += gflags_unittest
gflags_unittest_SOURCES = $(googleinclude_HEADERS) src/config.h \
	src/gflags_unittest.cc
gflags_unittest_CXXFLAGS = $(PTHREAD_CFLAGS)
gflags_unittest_LDFLAGS = $(PTHREAD_CFLAGS)
gflags_unittest_LDADD = libgflags.la $(PTHREAD_LIBS)

check_SCRIPTS += gflags_unittest_sh
noinst_SCRIPTS += src/gflags_unittest.sh
gflags_unittest_sh: gflags_unittest
	$(top_srcdir)/src/gflags_unittest.sh $(PWD)/$<

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
	libtool $(SCRIPTS)
