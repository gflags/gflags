## Process this file with autoconf to produce configure.
## In general, the safest way to proceed is to run ./autogen.sh

# make sure we're interpreted by some minimal autoconf
AC_PREREQ(2.57)

AC_INIT(gflags, 1.1, opensource@google.com)
# The argument here is just something that should be in the current directory
# (for sanity checking)
AC_CONFIG_SRCDIR(README)
AM_INIT_AUTOMAKE
AM_CONFIG_HEADER(src/config.h)

# Checks for programs.
AC_PROG_CC
AC_PROG_CPP
AC_PROG_CXX
AM_CONDITIONAL(GCC, test "$GCC" = yes)   # let the Makefile know if we're gcc
AC_CANONICAL_HOST

# Populate $host_cpu, $host_os, etc.
AC_CANONICAL_HOST
case $host_os in
  *mingw*)
    # Disabling fast install keeps libtool from creating wrapper scripts
    # around the executables it builds.  Such scripts have caused failures on
    # MinGW.  Using this option means an extra link step is executed during
    # "make install".
    AC_DISABLE_FAST_INSTALL
    ;;
    *)
    AC_ENABLE_FAST_INSTALL
    ;;
esac

# Uncomment this if you'll be exporting libraries (.so's)
AC_PROG_LIBTOOL
AC_SUBST(LIBTOOL_DEPS)

# Check whether some low-level functions/files are available
AC_HEADER_STDC

# These are tested for by AC_HEADER_STDC, but I check again to set the var
AC_CHECK_HEADER(stdint.h, ac_cv_have_stdint_h=1, ac_cv_have_stdint_h=0)
AC_CHECK_HEADER(sys/types.h, ac_cv_have_systypes_h=1, ac_cv_have_systypes_h=0)
AC_CHECK_HEADER(inttypes.h, ac_cv_have_inttypes_h=1, ac_cv_have_inttypes_h=0)
AC_CHECK_HEADERS([fnmatch.h])

# These are the types I need.  We look for them in either stdint.h,
# sys/types.h, or inttypes.h, all of which are part of the default-includes.
AC_CHECK_TYPE(uint16_t, ac_cv_have_uint16_t=1, ac_cv_have_uint16_t=0)
AC_CHECK_TYPE(u_int16_t, ac_cv_have_u_int16_t=1, ac_cv_have_u_int16_t=0)
AC_CHECK_TYPE(__int16, ac_cv_have___int16=1, ac_cv_have___int16=0)

AC_CHECK_FUNCS([strtoll strtoq])

AX_C___ATTRIBUTE__
# We only care about __attribute__ ((unused))
if test x"$ac_cv___attribute__" = x"yes"; then
  ac_cv___attribute__unused="__attribute__ ((unused))"
else
  ac_cv___attribute__unused=
fi

ACX_PTHREAD

# Find out what namespace 'normal' STL code lives in, and also what namespace
# the user wants our classes to be defined in
AC_CXX_STL_NAMESPACE
AC_DEFINE_GOOGLE_NAMESPACE(google)

# Solaris 10 6/06 has a bug where /usr/sfw/lib/libstdc++.la is empty.
# If so, we replace it with our own version.
LIBSTDCXX_LA_LINKER_FLAG=
if test -f /usr/sfw/lib/libstdc++.la && ! test -s /usr/sfw/lib/libstdc++.la
then
  LIBSTDCXX_LA_LINKER_FLAG='-L$(top_srcdir)/src/solaris'
fi
AC_SUBST(LIBSTDCXX_LA_LINKER_FLAG)

# These are what's needed by gflags.h.in
AC_SUBST(ac_google_start_namespace)
AC_SUBST(ac_google_end_namespace)
AC_SUBST(ac_google_namespace)
AC_SUBST(ac_cv___attribute__unused)
AC_SUBST(ac_cv_have_stdint_h)
AC_SUBST(ac_cv_have_systypes_h)
AC_SUBST(ac_cv_have_inttypes_h)
AC_SUBST(ac_cv_have_uint16_t)
AC_SUBST(ac_cv_have_u_int16_t)
AC_SUBST(ac_cv_have___int16)

## Check out ../autoconf/ for other macros you can call to do useful stuff

# Write generated configuration file, and also .h files
AC_CONFIG_FILES([Makefile src/gflags/gflags.h src/gflags/gflags_completions.h])
AC_OUTPUT
