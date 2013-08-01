## gflags tests

# ----------------------------------------------------------------------------
# output directories
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/bin")
set (CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/lib")
set (CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/lib")

set (TEMPDIR "${PROJECT_BINARY_DIR}/Testing/Temporary")

# ----------------------------------------------------------------------------
# common include directories and link libraries
include_directories ("${CMAKE_CURRENT_SOURCE_DIR}")
link_libraries (gflags_nothreads)

# ----------------------------------------------------------------------------
# test executables
configure_file (gflags_unittest.cc gflags_unittest-main.cc COPYONLY)
configure_file (gflags_unittest.cc gflags_unittest_main.cc COPYONLY)

add_executable (strip_flags gflags_strip_flags_test.cc)
add_executable (unittest    gflags_unittest.cc)
add_executable (unittest2   gflags_unittest-main.cc)
add_executable (unittest3   gflags_unittest_main.cc)

# ----------------------------------------------------------------------------
# test commands
add_test (
  NAME    strip_flags
  COMMAND /bin/bash "${CMAKE_CURRENT_SOURCE_DIR}/gflags_strip_flags_test.sh"
          "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/strip_flags"
)

add_test (
  NAME    unittest
  COMMAND /bin/bash "${CMAKE_CURRENT_SOURCE_DIR}/gflags_unittest.sh"
          "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/unittest"
          "${CMAKE_CURRENT_SOURCE_DIR}" # <srcdir>
          "${TEMPDIR}/unittest"         # <tempdir>
)
