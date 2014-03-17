## gflags tests

# ----------------------------------------------------------------------------
# output directories
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/bin")
set (CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/lib")
set (CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/lib")

# set working directory of test commands
set (GFLAGS_FLAGFILES_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

# ----------------------------------------------------------------------------
# common include directories and link libraries
include_directories ("${CMAKE_CURRENT_SOURCE_DIR}")
link_libraries (gflags_nothreads)

# ----------------------------------------------------------------------------
# STRIP_FLAG_HELP: check with "strings" that help text is not in binary
if (UNIX)
  add_executable (strip_flags gflags_strip_flags_test.cc)
  add_test (
    NAME    strip_flags
    COMMAND /bin/bash "${CMAKE_CURRENT_SOURCE_DIR}/gflags_strip_flags_test.sh"
            "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/strip_flags"
  )
endif ()

# ----------------------------------------------------------------------------
# unit tests
configure_file (gflags_unittest.cc gflags_unittest-main.cc COPYONLY)
configure_file (gflags_unittest.cc gflags_unittest_main.cc COPYONLY)

add_executable (unittest  gflags_unittest.cc)
add_executable (unittest2 gflags_unittest-main.cc)
add_executable (unittest3 gflags_unittest_main.cc)

# First, just make sure the unittest works as-is
add_gflags_test(unittest 0 "" "" unittest)

# --help should show all flags, including flags from gflags_reporting
add_gflags_test(help-reporting 1 "gflags_reporting.cc" "" unittest --help)

# Make sure that --help prints even very long helpstrings.
add_gflags_test(long-helpstring 1 "end of a long helpstring" "" unittest --help)

# Make sure --help reflects flag changes made before flag-parsing
add_gflags_test(changed_bool1 1 "-changed_bool1 (changed) type: bool default: true" "" unittest --help)
add_gflags_test(changed_bool2 1 "-changed_bool2 (changed) type: bool default: false currently: true" "" unittest --help)
# And on the command-line, too
add_gflags_test(changeable_string_var 1 "-changeable_string_var () type: string default: \"1\" currently: \"2\"" "" unittest --changeable_string_var 2 --help)

# --nohelp and --help=false should be as if we didn't say anything
add_gflags_test(nohelp     0 "PASS" "" unittest --nohelp)
add_gflags_test(help=false 0 "PASS" "" unittest --help=false)

# --helpfull is the same as help
add_gflags_test(helpfull 1 "gflags_reporting.cc" "" unittest --helpfull)

# --helpshort should show only flags from the unittest itself
add_gflags_test(helpshort 1 "gflags_unittest.cc" "gflags_reporting.cc" unittest --helpshort)

# --helpshort should show the tldflag we created in the unittest dir
add_gflags_test(helpshort-tldflag1 1 "tldflag1" "google.cc" unittest --helpshort)
add_gflags_test(helpshort-tldflag2 1 "tldflag2" "google.cc" unittest --helpshort)

# --helpshort should work if the main source file is suffixed with [_-]main
add_gflags_test(helpshort-main 1 "gflags_unittest-main.cc" "gflags_reporting.cc" unittest2 --helpshort)
add_gflags_test(helpshort_main 1 "gflags_unittest_main.cc" "gflags_reporting.cc" unittest3 --helpshort)

# --helpon needs an argument
add_gflags_test(helpon 1 "'--helpon' is missing its argument; flag description: show help on" "" unittest --helpon)

if (BUILD_SHARED_LIBS)
  # --helpon argument indicates what file we'll show args from
  # TODO(andreas): This test fails. Why is there no help for the gflags module ?
  add_gflags_test(helpon=gflags 1 "gflags.cc" "gflags_unittest.cc" unittest --helpon=gflags)
  # another way of specifying the argument
  # TODO(andreas): This test fails. Why is there no help for the gflags module ?
  add_gflags_test(helpon_gflags 1 "gflags.cc" "gflags_unittest.cc" unittest --helpon gflags)
endif ()

# test another argument
add_gflags_test(helpon=gflags_unittest 1 "gflags_unittest.cc" "gflags.cc" unittest --helpon=gflags_unittest)

# helpmatch is like helpon but takes substrings
add_gflags_test(helpmatch_reporting 1 "gflags_reporting.cc" "gflags_unittest.cc" unittest -helpmatch reporting)
add_gflags_test(helpmatch=unittest  1 "gflags_unittest.cc" "gflags.cc:" unittest -helpmatch=unittest)

# if no flags are found with helpmatch or helpon, suggest --help
add_gflags_test(helpmatch=nosuchsubstring 1 "No modules matched" "gflags_unittest.cc" unittest -helpmatch=nosuchsubstring)
add_gflags_test(helpon=nosuchmodule       1 "No modules matched" "gflags_unittest.cc" unittest -helpon=nosuchmodule)

# helppackage shows all the flags in the same dir as this unittest
# --help should show all flags, including flags from google.cc
add_gflags_test(helppackage 1 "gflags_reporting.cc" "" unittest --helppackage)

# xml!
add_gflags_test(helpxml 1 "gflags_unittest.cc</file>" "gflags_unittest.cc:" unittest --helpxml)

# just print the version info and exit
add_gflags_test(version-1 0 "gflags_unittest"      "gflags_unittest.cc" unittest --version)
add_gflags_test(version-2 0 "version test_version" "gflags_unittest.cc" unittest --version)

# --undefok is a fun flag...
add_gflags_test(undefok-1 1 "unknown command line flag 'foo'" "" unittest --undefok= --foo --unused_bool)
add_gflags_test(undefok-2 0 "PASS" "" unittest --undefok=foo --foo --unused_bool)
# If you say foo is ok to be undefined, we'll accept --nofoo as well
add_gflags_test(undefok-3 0 "PASS" "" unittest --undefok=foo --nofoo --unused_bool)
# It's ok if the foo is in the middle
add_gflags_test(undefok-4 0 "PASS" "" unittest --undefok=fee,fi,foo,fum --foo --unused_bool)
# But the spelling has to be just right...
add_gflags_test(undefok-5 1 "unknown command line flag 'foo'" "" unittest --undefok=fo --foo --unused_bool)
add_gflags_test(undefok-6 1 "unknown command line flag 'foo'" "" unittest --undefok=foot --foo --unused_bool)

# See if we can successfully load our flags from the flagfile
add_gflags_test(flagfile.1 0 "gflags_unittest" "gflags_unittest.cc" unittest "--flagfile=flagfile.1")
add_gflags_test(flagfile.2 0 "PASS" "" unittest "--flagfile=flagfile.2")
add_gflags_test(flagfile.3 0 "PASS" "" unittest "--flagfile=flagfile.3")

# Also try to load flags from the environment
add_gflags_test(fromenv=version      0 "gflags_unittest" "gflags_unittest.cc" unittest --fromenv=version)
add_gflags_test(tryfromenv=version   0 "gflags_unittest" "gflags_unittest.cc" unittest --tryfromenv=version)
add_gflags_test(fromenv=help         0 "PASS" "" unittest --fromenv=help)
add_gflags_test(tryfromenv=help      0 "PASS" "" unittest --tryfromenv=help)
add_gflags_test(fromenv=helpfull     1 "helpfull not found in environment" "" unittest --fromenv=helpfull)
add_gflags_test(tryfromenv=helpfull  0 "PASS" "" unittest --tryfromenv=helpfull)
add_gflags_test(tryfromenv=undefok   0 "PASS" "" unittest --tryfromenv=undefok --foo)
add_gflags_test(tryfromenv=weirdo    1 "unknown command line flag" "" unittest --tryfromenv=weirdo)
add_gflags_test(tryfromenv-multiple  0 "gflags_unittest" "gflags_unittest.cc" unittest --tryfromenv=test_bool,version,unused_bool)
add_gflags_test(fromenv=test_bool    1 "not found in environment" "" unittest --fromenv=test_bool)
add_gflags_test(fromenv=test_bool-ok 1 "unknown command line flag" "" unittest --fromenv=test_bool,ok)
# Here, the --version overrides the fromenv
add_gflags_test(version-overrides-fromenv 0 "gflags_unittest" "gflags_unittest.cc" unittest --fromenv=test_bool,version,ok)

# Make sure -- by itself stops argv processing
add_gflags_test(dashdash 0 "PASS" "" unittest -- --help)

# And we should die if the flag value doesn't pass the validator
add_gflags_test(always_fail 1 "ERROR: failed validation of new value 'true' for flag 'always_fail'" "" unittest --always_fail)

# And if locking in validators fails
# TODO(andreas): Worked on Windows 7 Release configuration, but causes
#                debugger abort() intervention in case of Debug configuration.
#add_gflags_test(deadlock_if_cant_lock 0 "PASS" "" unittest --deadlock_if_cant_lock)

# ----------------------------------------------------------------------------
# (negative) compilation tests
if (BUILD_NEGATIVE_COMPILATION_TESTS)
  find_package (PythonInterp)
  if (NOT PYTHON_EXECUTABLE)
    message (FATAL_ERROR "No Python installation found! It is required by the negative compilation tests."
                         " Either install Python or set NEGATIVE_COMPILATION_TESTS to FALSE and try again.")
  endif ()
  set (SRCDIR "${CMAKE_CURRENT_SOURCE_DIR}/nc")
  configure_file (gflags_nc.py.in "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/nc.py" @ONLY)
  macro (add_nc_test name)
    add_test (
      NAME nc_${name}
      COMMAND "${PYTHON_EXECUTABLE}" "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/nc.py" ${name}
    )
  endmacro ()
  add_nc_test (sanity)
  add_nc_test (swapped_args)
  add_nc_test (int_instead_of_bool)
  add_nc_test (bool_in_quotes)
  add_nc_test (define_string_with_0)
endif ()