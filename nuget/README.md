## Packaging gflags for Nuget

To create a nuget package for the gflags library: 

* Install the CoApp tools: http://downloads.coapp.org/files/Development.CoApp.Tools.Powershell.msi 
* Install VS 2010, 2012 and 2013.
* Run the BuildAndWriteNugetPackage.ps1 PS script from this folder.

This will create a nuget package for gflags that can be used from VS or CMake. CMake usage example:

In PS execute:

    PS> nuget install gflags -ExcludeVersion
    
Then in your CMakeLists.txt:

    cmake_minimum_required(VERSION 2.8.12)

    project(test_gflags)

    # make sure CMake finds the nuget installed package
    find_package(gflags REQUIRED)

    add_executable(test_gflags main.cpp)

    # gflags libraries are automatically mapped to the good arch/VS version/linkage combination
    target_link_libraries(test_gflags ${gflags_LIBRARIES})
    target_include_directories(test_gflags PRIVATE ${gflags_INCLUDE_DIR})

    # copy the DLL to the output folder if desired.
    if (MSVC AND COMMAND target_copy_shared_libs AND NOT gflags_STATIC)
      target_copy_shared_libs(test_gflags ${gflags_LIBRARIES})
    endif ()