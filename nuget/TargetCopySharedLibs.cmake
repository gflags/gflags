# - Copy shared library dependencies to output folder of target for Debug and Release configurations
#
# This can be used to emulate Nuget packages behaviour on Windows.
# WARNING: This macro was only tested on Windows and contains Windows specific code. It is a no-op if MSVC is not the actual compiler.
# TODO: Support all configurations
# Guillaume Dumont, 2014

macro(target_copy_shared_libs target )      
  if(MSVC)
    get_target_property (TARGET_LOCATION_DEBUG   ${target} LOCATION_Debug)
    get_target_property (TARGET_LOCATION_RELEASE ${target} LOCATION_Release)      
    if(TARGET_LOCATION_DEBUG AND TARGET_LOCATION_RELEASE)
      get_filename_component (TARGET_LOCATION_DEBUG "${TARGET_LOCATION_DEBUG}" PATH)
      get_filename_component (TARGET_LOCATION_RELEASE "${TARGET_LOCATION_RELEASE}" PATH)    
      
      foreach (_shared_lib ${ARGN})
          
        get_target_property( SHARED_LIB_LOCATION_DEBUG   ${_shared_lib} LOCATION_Debug)
        get_target_property( SHARED_LIB_LOCATION_RELEASE ${_shared_lib} LOCATION_Release)
        
        if (SHARED_LIB_LOCATION_DEBUG)
          get_filename_component(SHARED_LIB_EXT ${SHARED_LIB_LOCATION_DEBUG} EXT)
          if (SHARED_LIB_EXT MATCHES ".dll")
            set(IS_SHARED_LIB_DEBUG ON)
          endif ()
        endif ()
        
        if (SHARED_LIB_LOCATION_RELEASE)
          get_filename_component(SHARED_LIB_EXT ${SHARED_LIB_LOCATION_RELEASE} EXT)
          if (SHARED_LIB_EXT MATCHES ".dll")
            set(IS_SHARED_LIB_RELEASE ON)
          endif ()
        endif ()
        
        if (IS_SHARED_LIB_DEBUG AND IS_SHARED_LIB_RELEASE)
          
          add_custom_command( TARGET ${target} POST_BUILD
                              COMMAND ${CMAKE_COMMAND} -E copy_if_different $<$<CONFIG:Debug>:${SHARED_LIB_LOCATION_DEBUG}> $<$<CONFIG:Debug>:${TARGET_LOCATION_DEBUG}>
                                                                            $<$<NOT:$<CONFIG:Debug>>:${SHARED_LIB_LOCATION_RELEASE}> $<$<NOT:$<CONFIG:Debug>>:${TARGET_LOCATION_RELEASE}> 
                              )  
        else ()
          message( WARNING "Target {_shared_lib} could not be found or is not a DLL.")
        endif ()
      endforeach ()
    else ()
      message( WARNING "Could not find Debug and/or Release configurations for target: ${target}")
    endif ()
    endif()
endmacro()