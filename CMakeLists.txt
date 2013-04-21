cmake_minimum_required(VERSION 2.6 FATAL_ERROR)


# ----------------------------------------------------------------------------
# package information
set (PROJECT_NAME      "gflags")
set (PACKAGE_NAME      "${PROJECT_NAME}")
set (PACKAGE_VERSION   "2.1.0")
set (PACKAGE_STRING    "${PROJECT_NAME} ${PACKAGE_VERSION}")
set (PACKAGE_TARNAME   "${PROJECT_NAME}-${PACKAGE_VERSION}")
set (PACKAGE_BUGREPORT "https://code.google.com/p/gflags/issues/")

project (${PROJECT_NAME})

# ----------------------------------------------------------------------------
# configure options
option (BUILD_SHARED_LIBS "Request build of shared libraries." OFF)

set (GFLAGS_NAMESPACE "gflags" CACHE STRING "C++ namespace identifier of gflags library.")
mark_as_advanced (GFLAGS_NAMESPACE)

# ----------------------------------------------------------------------------
# source files - excluding root subdirectory and/or .in suffix
set (PUBLIC_HDRS
  "gflags/gflags.h"
  "gflags/gflags_declare.h"
  "gflags/gflags_completions.h"
)

set (PRIVATE_HDRS
  "config.h"
)

set (GFLAGS_SRCS
  "gflags.cc"
  "gflags_reporting.cc"
  "gflags_completions.cc"
)

# ----------------------------------------------------------------------------
# system checks
include (CheckTypeSize)
foreach (type IN ITEMS uint16_t u_int16_t __int16)
  CHECK_TYPE_SIZE (${type} SIZE)
  if (SIZE)
    set (HAVE_${type} 1)
  else ()
    set (HAVE_${type} 0)
  endif ()
endforeach ()

include (CheckIncludeFileCXX)
foreach (fname IN ITEMS fnmatch inttypes unistd sys/stat)
  string (TOUPPER "${fname}" FNAME)
  string (REGEX REPLACE "/" "_" FNAME "${FNAME}")
  CHECK_INCLUDE_FILE_CXX ("${fname}.h" HAVE_${FNAME}_H)
  if (HAVE_${FNAME}_H)
    set (HAVE_${FNAME}_H 1)
  else ()
    set (HAVE_${FNAME}_H 0)
  endif ()
endforeach ()

include (CheckSymbolExists)
foreach (fname IN ITEMS strtoll strtoq)
  string (TOUPPER "${fname}" FNAME)
  CHECK_SYMBOL_EXISTS ("${fname}" stdlib.h HAVE_${FNAME})
  if (HAVE_${FNAME})
    set (HAVE_${FNAME} 1)
  else ()
    set (HAVE_${FNAME} 0)
  endif ()
endforeach ()

find_package (Threads)
if (Threads_FOUND)
  if (CMAKE_USE_PTHREADS_INIT)
    set (HAVE_PTHREAD 1)
  else  ()
    set (HAVE_PTHREAD 0)
  endif ()
endif ()

# ----------------------------------------------------------------------------
# configure source files
if (CMAKE_COMPILER_IS_GNUCXX)
  set (__ATTRIBUTE__UNUSED "__attribute((unused))")
else ()
  set (__ATTRIBUTE__UNUSED)
endif ()

function (configure_sources out subdir)
  set (tmp)
  foreach (src IN LISTS ARGN)
    set (src "${subdir}/${src}")
    if (EXISTS "${PROJECT_SOURCE_DIR}/${src}.in")
      configure_file ("${PROJECT_SOURCE_DIR}/${src}.in" "${PROJECT_BINARY_DIR}/${src}" @ONLY)
      list (APPEND tmp "${PROJECT_BINARY_DIR}/${src}")
    else ()
      list (APPEND tmp "${PROJECT_SOURCE_DIR}/${src}")
    endif ()
  endforeach ()
  set (${out} "${tmp}" PARENT_SCOPE)
endfunction ()

configure_sources (PUBLIC_HDRS  include ${PUBLIC_HDRS})
configure_sources (PRIVATE_HDRS src     ${PRIVATE_HDRS})
configure_sources (GFLAGS_SRCS  src     ${GFLAGS_SRCS})

# ----------------------------------------------------------------------------
# output directories
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY "bin")
set (CMAKE_LIBRARY_OUTPUT_DIRECTORY "lib")
set (CMAKE_ARCHIVE_OUTPUT_DIRECTORY "lib")

# ----------------------------------------------------------------------------
# add library target
include_directories (
  "${PROJECT_BINARY_DIR}/include"
  "${PROJECT_SOURCE_DIR}/include"
  "${PROJECT_BINARY_DIR}/src"
  "${PROJECT_SOURCE_DIR}/src"
)

if (WIN32)
  add_definitions (-DGFLAGS_DLL_EXPORT)
endif ()

add_library (gflags ${GFLAGS_SRCS})

# ----------------------------------------------------------------------------
# installation
install (TARGETS gflags DESTINATION lib)
install (FILES ${PUBLIC_HDRS} DESTINATION include/gflags)
