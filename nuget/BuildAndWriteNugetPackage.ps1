function BuildPivot( $source_dir, $build_dir, $generator, $options ) {
    if(!(Test-Path -Path $build_dir )){
        mkdir $build_dir
    }

    pushd $build_dir 
    cmake -G $generator $options -DCMAKE_INSTALL_PREFIX=install $source_dir
    cmake --build . --target INSTALL --config Debug
    cmake --build . --target INSTALL --config Release
    popd
}

$source_dir   = "$PSScriptRoot\.."

# VS 2013
#######################################################
$build_dir = "./build/x64/v120/static"
$generator = "Visual Studio 12 Win64"
$options ="-DBUILD_SHARED_LIBS=OFF"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/x64/v120/dynamic"
$generator = "Visual Studio 12 Win64"
$options ="-DBUILD_SHARED_LIBS=ON"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/Win32/v120/static"
$generator = "Visual Studio 12"
$options ="-DBUILD_SHARED_LIBS=OFF"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/Win32/v120/dynamic"
$generator = "Visual Studio 12"
$options ="-DBUILD_SHARED_LIBS=ON"

BuildPivot $source_dir $build_dir $generator $options

#######################################################

# VS 2012
#######################################################
$build_dir = "./build/x64/v110/static"
$generator = "Visual Studio 11 Win64"
$options ="-DBUILD_SHARED_LIBS=OFF"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/x64/v110/dynamic"
$generator = "Visual Studio 11 Win64"
$options ="-DBUILD_SHARED_LIBS=ON"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/Win32/v110/static"
$generator = "Visual Studio 11"
$options ="-DBUILD_SHARED_LIBS=OFF"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/Win32/v110/dynamic"
$generator = "Visual Studio 11"
$options ="-DBUILD_SHARED_LIBS=ON"

BuildPivot $source_dir $build_dir $generator $options
#######################################################

# VS 2010
#######################################################
$build_dir = "./build/x64/v100/static"
$generator = "Visual Studio 10 Win64"
$options ="-DBUILD_SHARED_LIBS=OFF"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/x64/v100/dynamic"
$generator = "Visual Studio 10 Win64"
$options ="-DBUILD_SHARED_LIBS=ON"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/Win32/v100/static"
$generator = "Visual Studio 10"
$options ="-DBUILD_SHARED_LIBS=OFF"

BuildPivot $source_dir $build_dir $generator $options

$build_dir = "./build/Win32/v100/dynamic"
$generator = "Visual Studio 10"
$options ="-DBUILD_SHARED_LIBS=ON"

BuildPivot $source_dir $build_dir $generator $options
#######################################################

Write-NuGetPackage  -SplitThreshold 10000000 .\gflags.autopkg



