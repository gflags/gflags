## @file  utils.cmake
#  @brief Utility CMake functions.

# ----------------------------------------------------------------------------
## @brief Extract version numbers from version string.
#
# @param [in]  VERSION Version string in the format "MAJOR[.MINOR[.PATCH]]".
# @param [out] MAJOR   Major version number if given or 0.
# @param [out] MINOR   Minor version number if given or 0.
# @param [out] PATCH   Patch number if given or 0.
#
# @returns See @c [out] parameters.
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
