## This is a boilerplate file for Google opensource projects.
## To make it useful, replace <<TEXT>> with actual text for your project.
## Also, look at comments with "## double hashes" to see if any are worth
## uncommenting or modifying.

## Process this file with autoconf to produce configure.
## In general, the safest way to proceed is to run the following:
##    % aclocal -I . -I `pwd`/../autoconf && autoheader && autoconf && automake

# make sure we're interpreted by some minimal autoconf
AC_PREREQ(2.57)

AC_INIT(gflags, 0.4, opensource@google.com)
# The argument here is just something that should be in the current directory
# (for sanity checking)
AC_CONFIG_SRCDIR(README)
AM_INIT_AUTOMAKE
AM_CONFIG_HEADER(src/config.h)

# Checks for programs.
AC_PROG_CC
AC_PROG_CPP
AC_PROG_CXX

# Uncomment this if you'll be exporting libraries (.so's)
AC_PROG_LIBTOOL
AC_SUBST(LIBTOOL_DEPS)

# Check whether some low-level functions/files are available
AC_HEADER_STDC

# These are tested for by AC_HEADER_STDC, but I check again to set the var
AC_CHECK_HEADER(stdint.h, ac_cv_have_stdint_h=1, ac_cv_have_stdint_h=0)
AC_CHECK_HEADER(sys/types.h, ac_cv_have_systypes_h=1, ac_cv_have_systypes_h=0)
AC_CHECK_HEADER(inttypes.h, ac_cv_have_inttypes_h=1, ac_cv_have_inttypes_h=0)

# These are the types I need.  We look for them in either stdint.h,
# sys/types.h, or inttypes.h, all of which are part of the default-includes.
AC_CHECK_TYPE(uint16_t, ac_cv_have_uint16_t=1, ac_cv_have_uint16_t=0)
AC_CHECK_TYPE(u_int16_t, ac_cv_have_u_int16_t=1, ac_cv_have_u_int16_t=0)
AC_CHECK_TYPE(__uint16, ac_cv_have___uint16=1, ac_cv_have___uint16=0)

AC_CHECK_FUNCS(strtoll)
AC_CHECK_FUNCS(strtoq)

AX_C___ATTRIBUTE__
ACX_PTHREAD

# Find out what namespace 'normal' STL code lives in, and also what namespace
# the user wants our classes to be defined in
AC_CXX_STL_NAMESPACE
AC_DEFINE_GOOGLE_NAMESPACE(google)

# These are what's needed by gflags.h.in
AC_SUBST(ac_google_start_namespace)
AC_SUBST(ac_google_end_namespace)
AC_SUBST(ac_google_namespace)
AC_SUBST(ac_cv___attribute__)
AC_SUBST(ac_cv_have_stdint_h)
AC_SUBST(ac_cv_have_systypes_h)
AC_SUBST(ac_cv_have_inttypes_h)
AC_SUBST(ac_cv_have_uint16_t)
AC_SUBST(ac_cv_have_u_int16_t)
AC_SUBST(ac_cv_have___uint16)

## Check out ../autoconf/ for other macros you can call to do useful stuff

# Write generated configuration file, and also .h files
AC_CONFIG_FILES([Makefile src/google/gflags.h])
AC_OUTPUT
