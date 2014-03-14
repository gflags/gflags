## Utility CMake functions.

# ----------------------------------------------------------------------------
## Extract version numbers from version string.
function (version_numbers VERSION MAJOR MINOR PATCH)
  if (VERSION MATCHES "([0-9]+)(\\.[0-9]+)?(\\.[0-9]+)?(rc[1-9][0-9]*|[a-z]+)?")
    if (CMAKE_MATCH_1)
      set (VERSION_MAJOR ${CMAKE_MATCH_1})
    else ()
      set (VERSION_MAJOR 0)
    endif ()
    if (CMAKE_MATCH_2)
      set (VERSION_MINOR ${CMAKE_MATCH_2})
      string (REGEX REPLACE "^\\." "" VERSION_MINOR "${VERSION_MINOR}")
    else ()
      set (VERSION_MINOR 0)
    endif ()
    if (CMAKE_MATCH_3)
      set (VERSION_PATCH ${CMAKE_MATCH_3})
      string (REGEX REPLACE "^\\." "" VERSION_PATCH "${VERSION_PATCH}")
    else ()
      set (VERSION_PATCH 0)
    endif ()
  else ()
    set (VERSION_MAJOR 0)
    set (VERSION_MINOR 0)
    set (VERSION_PATCH 0)
  endif ()
  set ("${MAJOR}" "${VERSION_MAJOR}" PARENT_SCOPE)
  set ("${MINOR}" "${VERSION_MINOR}" PARENT_SCOPE)
  set ("${PATCH}" "${VERSION_PATCH}" PARENT_SCOPE)
endfunction ()

# ----------------------------------------------------------------------------
## Configure public header files
function (configure_headers out)
  set (tmp)
  foreach (src IN LISTS ARGN)
    if (EXISTS "${PROJECT_SOURCE_DIR}/src/${src}.in")
      configure_file ("${PROJECT_SOURCE_DIR}/src/${src}.in" "${PROJECT_BINARY_DIR}/include/${GFLAGS_NAMESPACE}/${src}" @ONLY)
      list (APPEND tmp "${PROJECT_BINARY_DIR}/include/${GFLAGS_NAMESPACE}/${src}")
    else ()
	    configure_file ("${PROJECT_SOURCE_DIR}/src/${src}" "${PROJECT_BINARY_DIR}/include/${GFLAGS_NAMESPACE}/${src}" COPYONLY)
      list (APPEND tmp "${PROJECT_BINARY_DIR}/include/${GFLAGS_NAMESPACE}/${src}")
    endif ()
  endforeach ()
  set (${out} "${tmp}" PARENT_SCOPE)
endfunction ()

# ----------------------------------------------------------------------------
## Configure source files with .in suffix
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

# ----------------------------------------------------------------------------
## Add usage test
#
# Using PASS_REGULAR_EXPRESSION and FAIL_REGULAR_EXPRESSION would
# do as well, but CMake/CTest does not allow us to specify an
# expected exist status. Moreover, the execute_test.cmake script
# sets environment variables needed by the --fromenv/--tryfromenv tests.
macro (add_gflags_test name expected_rc expected_output unexpected_output cmd)
  add_test (
    NAME    ${name}
    COMMAND "${CMAKE_COMMAND}" "-DCOMMAND:STRING=$<TARGET_FILE:${cmd}>;${ARGN}"
                               "-DEXPECTED_RC:STRING=${expected_rc}"
                               "-DEXPECTED_OUTPUT:STRING=${expected_output}"
                               "-DUNEXPECTED_OUTPUT:STRING=${unexpected_output}"
                               -P "${PROJECT_SOURCE_DIR}/test/execute_test.cmake"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/test"
  )
endmacro ()
