## gflags tests

# ----------------------------------------------------------------------------
# output directories
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/bin")
set (CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/lib")
set (CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/Testing/lib")

set (TEMPDIR "${PROJECT_BINARY_DIR}/Testing/Temporary")

# ----------------------------------------------------------------------------
# common link libraries
link_libraries (gflags)

# ----------------------------------------------------------------------------
# test executables
add_executable (strip_flags gflags_strip_flags_test.cc)
add_executable (unittest    gflags_unittest.cc)

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
