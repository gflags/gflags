# - Nuget specific gflags-config cmake file
#
# This wrap the inclusion of the true gflags-config.cmake 
# so that the nuget package can be used from cmake as well.
# This files takes care of mapping the gflags-config to the proper
# architecture/compiler/linkage version of the library.
# Guillaume Dumont, 2014

if(NOT DEFINED gflags_STATIC)
  # look for global setting
  if(NOT DEFINED BUILD_SHARED_LIBS OR BUILD_SHARED_LIBS)
    option (gflags_STATIC "Link to static gflags name" OFF)
  else()
    option (gflags_STATIC "Link to static gflags name" ON)
  endif()
endif()

# Determine if we link to static or shared libraries
if (gflags_STATIC)
  set (MSVC_LINKAGE static)
else()
  set (MSVC_LINKAGE dynamic)
endif()

# Determine architecture
if (CMAKE_CL_64)
  set (MSVC_ARCH x64)
else ()
  set (MSVC_ARCH Win32)
endif ()

# Determine VS version
set (MSVC_VERSIONS 1600 1700 1800)
set (MSVC_TOOLSETS v100 v110 v120)

list (LENGTH MSVC_VERSIONS N_VERSIONS)
math (EXPR N_LOOP "${N_VERSIONS} - 1")

foreach (i RANGE ${N_LOOP})        
  list (GET MSVC_VERSIONS ${i} _msvc_version)
  if (_msvc_version EQUAL MSVC_VERSION)
    list (GET MSVC_TOOLSETS ${i} MSVC_TOOLSET)
  endif ()    
endforeach () 
if (NOT MSVC_TOOLSET)
  message( WARNING "Could not find binaries matching your compiler version. Defaulting to v120." )
  set( MSVC_TOOLSET v120 )
endif ()

get_filename_component (CMAKE_CURRENT_LIST_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)

# Include CMake generated configuration file for proper config
include ("${CMAKE_CURRENT_LIST_DIR}/build/native/${MSVC_ARCH}/${MSVC_TOOLSET}/${MSVC_LINKAGE}/CMake/gflags-config.cmake")

# overwrite include directory. CMake points to a directory which is not existent in the nuget package
set (gflags_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/build/native/include")

# Redefine this as well since target names do not match
# actual binaries.
if (gflags_STATIC)
  set (gflags_LIBRARIES gflags-static)
else ()
  set (gflags_LIBRARIES gflags-shared)  
endif()

# include a macro that makes it easy to copy gflags DLLs to output folder.
include("${CMAKE_CURRENT_LIST_DIR}/TargetCopySharedLibs.cmake")