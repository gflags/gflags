## gflags negative compilation tests

cmake_minimum_required (VERSION 2.8)

if (NOT TEST_NAME)
  message (FATAL_ERROR "Missing TEST_NAME CMake flag")
endif ()
string (TOUPPER ${TEST_NAME} TEST_NAME_UPPER)

project (gflags_nc_${TEST_NAME})

find_package (gflags REQUIRED)
include_directories (${gflags_INCLUDE_DIR} "${CMAKE_CURRENT_SOURCE_DIR}/..")
link_libraries (gflags_nothreads)
add_definitions (-DTEST_${TEST_NAME_UPPER})
add_executable (gflags_nc_${TEST_NAME} gflags_nc.cc)
