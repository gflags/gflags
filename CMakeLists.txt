cmake_minimum_required(VERSION 2.8.4 FATAL_ERROR)

if (WIN32 AND NOT CYGWIN)
  set (WINDOWS 1)
else ()
  set (WINDOWS 0)
endif ()

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

project (${PROJECT_NAME} CXX)

version_numbers (
  ${PACKAGE_VERSION}
    PACKAGE_VERSION_MAJOR
    PACKAGE_VERSION_MINOR
    PACKAGE_VERSION_PATCH
)

# ----------------------------------------------------------------------------
# configure options
option (BUILD_SHARED_LIBS "Request build of shared libraries." OFF)

if (WINDOWS AND BUILD_SHARED_LIBS)
  set (GFLAGS_IS_A_DLL 1)
else ()
  set (GFLAGS_IS_A_DLL 0)
endif ()

option (BUILD_gflags_LIB           "Request build of the multi-threaded gflags library."  ON)
option (BUILD_gflags_nothreads_LIB "Request build of the single-threaded gflags library." ON)

if (NOT BUILD_gflags_LIB AND NOT BUILD_gflags_nothreads_LIB)
 message (FATAL_ERROR "At least one of BUILD_gflags_LIB and BUILD_gflags_nothreads_LIB must be ON.")
endif ()

option (BUILD_NEGATIVE_COMPILATION_TESTS "Request addition of negative compilation tests." OFF)
mark_as_advanced (BUILD_NEGATIVE_COMPILATION_TESTS)

set (GFLAGS_NAMESPACE "gflags" CACHE STRING "C++ namespace identifier of gflags library.")
mark_as_advanced (GFLAGS_NAMESPACE)

mark_as_advanced (CLEAR CMAKE_INSTALL_PREFIX)
mark_as_advanced (CMAKE_CONFIGURATION_TYPES)
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CXX_FLAGS AND NOT CMAKE_C_FLAGS)
  set (
    CMAKE_BUILD_TYPE "Release"
    CACHE STRING "Choose the type of build, options are: None (CMAKE_C_FLAGS and CMAKE_CXX_FLAGS used) Debug Release RelWithDebInfo MinSizeRel."
    FORCE
  )
endif ()

if (APPLE)
  mark_as_advanced(CMAKE_OSX_ARCHITECTURES
                   CMAKE_OSX_DEPLOYMENT_TARGET
                   CMAKE_OSX_SYSROOT)
endif ()

# ----------------------------------------------------------------------------
# system checks
include (CheckTypeSize)
include (CheckIncludeFileCXX)
include (CheckCXXSymbolExists)

if (MSVC)
  set (HAVE_SYS_TYPES_H 1)
  set (HAVE_STDINT_H    1)
  set (HAVE_STDDEF_H    1) # used by CheckTypeSize module
  set (HAVE_INTTYPES_H  0)
  set (HAVE_UNISTD_H    0)
  set (HAVE_SYS_STAT_H  1)
  check_include_file_cxx ("shlwapi.h" HAVE_SHLWAPI_H)
else ()
  foreach (fname IN ITEMS unistd stdint inttypes sys/types sys/stat fnmatch)
    string (TOUPPER "${fname}" FNAME)
    string (REGEX REPLACE "/" "_" FNAME "${FNAME}")
    if (NOT HAVE_${FNAME}_H)
      check_include_file_cxx ("${fname}.h" HAVE_${FNAME}_H)
    endif ()
  endforeach ()
  # the following are used in #if not #ifdef
  bool_to_int (HAVE_STDINT_H)
  bool_to_int (HAVE_SYS_TYPES_H)
  bool_to_int (HAVE_INTTYPES_H)
endif ()

set (GFLAGS_INTTYPES_FORMAT "" CACHE STRING "Format of integer types: \"C99\" (uint32_t), \"BSD\" (u_int32_t), \"VC7\" (__int32)")
set_property (CACHE GFLAGS_INTTYPES_FORMAT PROPERTY STRINGS "C99;BSD;VC7")
mark_as_advanced (GFLAGS_INTTYPES_FORMAT)
if (NOT GFLAGS_INTTYPES_FORMAT)
  set (TYPES uint32_t u_int32_t)
  if (MSVC)
    list (INSERT TYPES 0 __int32)
  endif ()
  foreach (type IN LISTS TYPES)
    check_type_size (${type} ${type} LANGUAGE CXX)
    if (HAVE_${type})
      break ()
    endif ()
  endforeach ()
  if (HAVE_uint32_t)
    set_property (CACHE GFLAGS_INTTYPES_FORMAT PROPERTY VALUE C99)
  elseif (HAVE_u_int32_t)
    set_property (CACHE GFLAGS_INTTYPES_FORMAT PROPERTY VALUE BSD)
  elseif (HAVE___int32)
    set_property (CACHE GFLAGS_INTTYPES_FORMAT PROPERTY VALUE VC7)
  else ()
    mark_as_advanced (CLEAR GFLAGS_INTTYPES_FORMAT)
    message (FATAL_ERROR "Do not know how to define a 32-bit integer quantity on your system!"
                         " Neither uint32_t, u_int32_t, nor __int32 seem to be available."
                         " Set GFLAGS_INTTYPES_FORMAT to either C99, BSD, or VC7 and try again.")
  endif ()
endif ()
# use of special characters in strings to circumvent bug #0008226
if ("^${GFLAGS_INTTYPES_FORMAT}$" STREQUAL "^WIN$")
  set_property (CACHE GFLAGS_INTTYPES_FORMAT PROPERTY VALUE VC7)
endif ()
if (NOT GFLAGS_INTTYPES_FORMAT MATCHES "^(C99|BSD|VC7)$")
  message (FATAL_ERROR "Invalid value for GFLAGS_INTTYPES_FORMAT! Choose one of \"C99\", \"BSD\", or \"VC7\"")
endif ()
set (GFLAGS_INTTYPES_FORMAT_C99 0)
set (GFLAGS_INTTYPES_FORMAT_BSD 0)
set (GFLAGS_INTTYPES_FORMAT_VC7 0)
set ("GFLAGS_INTTYPES_FORMAT_${GFLAGS_INTTYPES_FORMAT}" 1)

if (MSVC)
  set (HAVE_strtoll 0)
  set (HAVE_strtoq  0)
else ()
  check_cxx_symbol_exists (strtoll stdlib.h HAVE_STRTOLL)
  if (NOT HAVE_STRTOLL)
    check_cxx_symbol_exists (strtoq stdlib.h HAVE_STRTOQ)
  endif ()
endif ()

set (CMAKE_THREAD_PREFER_PTHREAD TRUE)
find_package (ThreadsCXX)
if (Threads_FOUND AND CMAKE_USE_PTHREADS_INIT)
  set (HAVE_PTHREAD 1)
  check_type_size (pthread_rwlock_t RWLOCK LANGUAGE CXX)
else ()
  set (HAVE_PTHREAD 0)
endif ()

if (UNIX AND NOT HAVE_PTHREAD AND BUILD_gflags_LIB)
  if (CMAKE_HAVE_PTHREAD_H)
    set (what "library")
  else ()
    set (what ".h file")
  endif ()
  message (FATAL_ERROR "Could not find pthread${what}. Check the log file"
                       "\n\t${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeError.log"
                       "\nor disable the build of the multi-threaded gflags library (BUILD_gflags_LIB=OFF).")
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

if (WINDOWS)
  list (APPEND PRIVATE_HDRS "windows_port.h")
  list (APPEND GFLAGS_SRCS  "windows_port.cc")
endif ()

# ----------------------------------------------------------------------------
# configure source files
if (CMAKE_COMPILER_IS_GNUCXX)
  set (GFLAGS_ATTRIBUTE_UNUSED "__attribute((unused))")
else ()
  set (GFLAGS_ATTRIBUTE_UNUSED)
endif ()

configure_headers (PUBLIC_HDRS  ${PUBLIC_HDRS})
configure_sources (PRIVATE_HDRS ${PRIVATE_HDRS})
configure_sources (GFLAGS_SRCS  ${GFLAGS_SRCS})

# ----------------------------------------------------------------------------
# output directories
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY "bin")
set (CMAKE_LIBRARY_OUTPUT_DIRECTORY "lib")
set (CMAKE_ARCHIVE_OUTPUT_DIRECTORY "lib")

# ----------------------------------------------------------------------------
# add library target
include_directories ("${PROJECT_SOURCE_DIR}/src")
include_directories ("${PROJECT_BINARY_DIR}/include")
include_directories ("${PROJECT_BINARY_DIR}/include/${GFLAGS_NAMESPACE}")

set (LIB_TARGETS)
if (BUILD_gflags_LIB)
  add_library (gflags ${GFLAGS_SRCS} ${PRIVATE_HDRS} ${PUBLIC_HDRS})
  list (APPEND LIB_TARGETS gflags)
endif ()
if (BUILD_gflags_nothreads_LIB)
  add_library (gflags_nothreads ${GFLAGS_SRCS} ${PRIVATE_HDRS} ${PUBLIC_HDRS})
  set_target_properties (gflags_nothreads PROPERTIES COMPILE_DEFINITIONS NO_THREADS)
  list (APPEND LIB_TARGETS gflags_nothreads)
endif ()

# ----------------------------------------------------------------------------
# installation
if (WINDOWS)
  set (RUNTIME_INSTALL_DIR Bin)
  set (LIBRARY_INSTALL_DIR Lib)
  set (INCLUDE_INSTALL_DIR Include)
  set (CONFIG_INSTALL_DIR  CMake)
else ()
  set (RUNTIME_INSTALL_DIR bin)
  set (LIBRARY_INSTALL_DIR lib)
  set (INCLUDE_INSTALL_DIR include)
  set (CONFIG_INSTALL_DIR  lib/cmake/${PACKAGE_NAME})
endif ()

install (TARGETS ${LIB_TARGETS} DESTINATION ${LIBRARY_INSTALL_DIR} EXPORT gflags-lib)
install (FILES   ${PUBLIC_HDRS} DESTINATION ${INCLUDE_INSTALL_DIR}/${GFLAGS_NAMESPACE})

file (RELATIVE_PATH INSTALL_PREFIX_REL2CONFIG_DIR "${CMAKE_INSTALL_PREFIX}/${CONFIG_INSTALL_DIR}" "${CMAKE_INSTALL_PREFIX}")
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

if (UNIX)
  install (PROGRAMS src/gflags_completions.sh DESTINATION ${RUNTIME_INSTALL_DIR})
endif ()

# ----------------------------------------------------------------------------
# support direct use of build tree
set (INSTALL_PREFIX_REL2CONFIG_DIR .)
export (TARGETS ${LIB_TARGETS} FILE "${PROJECT_BINARY_DIR}/${PACKAGE_NAME}-export.cmake")
export (PACKAGE gflags)
configure_file (cmake/config.cmake.in "${PROJECT_BINARY_DIR}/${PACKAGE_NAME}-config.cmake" @ONLY)

# ----------------------------------------------------------------------------
# testing - MUST follow the generation of the build tree config file
include (CTest)
if (BUILD_TESTING)
  enable_testing ()
  add_subdirectory (test)
endif ()
