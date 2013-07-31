cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

# ----------------------------------------------------------------------------
# includes
set (CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include (utils)

# ----------------------------------------------------------------------------
# package information
set (PROJECT_NAME      "gflags")
set (PACKAGE_NAME      "${PROJECT_NAME}")
set (PACKAGE_VERSION   "2.1.0")
set (PACKAGE_STRING    "${PROJECT_NAME} ${PACKAGE_VERSION}")
set (PACKAGE_TARNAME   "${PROJECT_NAME}-${PACKAGE_VERSION}")
set (PACKAGE_BUGREPORT "https://code.google.com/p/gflags/issues/")

project (${PROJECT_NAME})

version_numbers (
  ${PACKAGE_VERSION}
    PACKAGE_VERSION_MAJOR
    PACKAGE_VERSION_MINOR
    PACKAGE_VERSION_PATCH
)

# ----------------------------------------------------------------------------
# configure options
option (BUILD_SHARED_LIBS "Request build of shared libraries." OFF)

set (GFLAGS_NAMESPACE "gflags" CACHE STRING "C++ namespace identifier of gflags library.")
mark_as_advanced (GFLAGS_NAMESPACE)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CXX_FLAGS AND NOT CMAKE_C_FLAGS)
  set (
    CMAKE_BUILD_TYPE "Release"
    CACHE STRING "Choose the type of build, options are: None (CMAKE_C_FLAGS and CMAKE_CXX_FLAGS used) Debug Release RelWithDebInfo MinSizeRel."
    FORCE
  )
endif ()

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
# source files - excluding root subdirectory and/or .in suffix
set (PUBLIC_HDRS
  "gflags.h"
  "gflags_declare.h"
  "gflags_completions.h"
)

set (PRIVATE_HDRS
  "config.h"
)

set (GFLAGS_SRCS
  "gflags.cc"
  "gflags_reporting.cc"
  "gflags_completions.cc"
)

if (WIN32)
  list (APPEND PRIVATE_HDRS "windows_port.h")
  list (APPEND GFLAGS_SRCS  "windows_port.cc")
endif ()

# ----------------------------------------------------------------------------
# configure source files
if (CMAKE_COMPILER_IS_GNUCXX)
  set (__ATTRIBUTE__UNUSED "__attribute((unused))")
else ()
  set (__ATTRIBUTE__UNUSED)
endif ()

function (configure_sources out)
  set (tmp)
  foreach (src IN LISTS ARGN)
    if (src MATCHES ".h$" AND EXISTS "${PROJECT_SOURCE_DIR}/src/${src}.in")
      configure_file ("${PROJECT_SOURCE_DIR}/src/${src}.in" "${PROJECT_BINARY_DIR}/include/${GFLAGS_NAMESPACE}/${src}" @ONLY)
      list (APPEND tmp "${PROJECT_BINARY_DIR}/include/${GFLAGS_NAMESPACE}/${src}")
    else ()
      list (APPEND tmp "${PROJECT_SOURCE_DIR}/src/${src}")
    endif ()
  endforeach ()
  set (${out} "${tmp}" PARENT_SCOPE)
endfunction ()

configure_sources (PUBLIC_HDRS  ${PUBLIC_HDRS})
configure_sources (PRIVATE_HDRS ${PRIVATE_HDRS})
configure_sources (GFLAGS_SRCS  ${GFLAGS_SRCS})

# ----------------------------------------------------------------------------
# output directories
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY "bin")
set (CMAKE_LIBRARY_OUTPUT_DIRECTORY "lib")
set (CMAKE_ARCHIVE_OUTPUT_DIRECTORY "lib")

# ----------------------------------------------------------------------------
# add library target
if (WIN32)
  add_definitions (-DGFLAGS_DLL_EXPORT)
endif ()
include_directories ("${PROJECT_SOURCE_DIR}/src")
include_directories ("${PROJECT_BINARY_DIR}/include")
include_directories ("${PROJECT_BINARY_DIR}/include/${GFLAGS_NAMESPACE}")
add_library (gflags ${GFLAGS_SRCS})

# ----------------------------------------------------------------------------
# installation
if (WIN32)
  set (LIBRARY_INSTALL_DIR Lib)
  set (INCLUDE_INSTALL_DIR Include)
  set (CONFIG_INSTALL_DIR  CMake)
else ()
  set (LIBRARY_INSTALL_DIR lib)
  set (INCLUDE_INSTALL_DIR include)
  set (CONFIG_INSTALL_DIR  cmake/${PACKAGE_NAME})
endif ()

install (TARGETS ${PACKAGE_NAME} DESTINATION ${LIBRARY_INSTALL_DIR} EXPORT gflags-lib)
install (FILES   ${PUBLIC_HDRS}  DESTINATION ${INCLUDE_INSTALL_DIR}/${GFLAGS_NAMESPACE})

file (RELATIVE_PATH INSTALL_PREFIX_REL2CONFIG_DIR "${CMAKE_INSTALL_PREFIX}" "${CMAKE_INSTALL_PREFIX}/${CONFIG_INSTALL_DIR}")
configure_file (cmake/config.cmake.in  "${PROJECT_BINARY_DIR}/${PACKAGE_NAME}-config-install.cmake" @ONLY)
configure_file (cmake/version.cmake.in "${PROJECT_BINARY_DIR}/${PACKAGE_NAME}-config-version.cmake" @ONLY)

install (
  FILES "${PROJECT_BINARY_DIR}/${PACKAGE_NAME}-config-install.cmake"
  RENAME ${PACKAGE_NAME}-config.cmake
  DESTINATION ${CONFIG_INSTALL_DIR}
)

install (
  FILES "${PROJECT_BINARY_DIR}/${PACKAGE_NAME}-config-version.cmake"
  DESTINATION ${CONFIG_INSTALL_DIR}
)

install (EXPORT gflags-lib DESTINATION ${CONFIG_INSTALL_DIR} FILE ${PACKAGE_NAME}-export.cmake)

# ----------------------------------------------------------------------------
# support direct use of build tree
set (INSTALL_PREFIX_REL2CONFIG_DIR .)
export (TARGETS gflags FILE "${PROJECT_BINARY_DIR}/${PACKAGE_NAME}-export.cmake")
configure_file (cmake/config.cmake.in "${PROJECT_BINARY_DIR}/${PACKAGE_NAME}-config.cmake" @ONLY)
