Installing a binary distribution package
========================================

No official binary distribution packages are provided by the gflags developers.
There may, however, be binary packages available for your OS. Please consult
also the package repositories of your Linux distribution.

For example on Debian/Ubuntu Linux, gflags can be installed using the
following command:

    sudo apt-get install gflags


Compiling the source code
=========================

The build system of gflags is since version 2.1 based on [CMake](http://cmake.org).
The common steps to build, test, and install software are therefore:

1. Extract source files.
2. Create build directory and change to it.
3. Run CMake to configure the build tree.
4. Build the software using selected build tool.
5. Test the built software.
6. Install the built files.

On Unix-like systems with GNU Make as build tool, these build steps can be
summarized by the following sequence of commands executed in a shell,
where ```$package``` and ```$version``` are shell variables which represent
the name of this package and the obtained version of the software.

    $ tar xzf gflags-$version-source.tar.gz
    $ cd gflags-$version
    $ mkdir build && cd build
    $ ccmake ..
    
      - Press 'c' to configure the build system and 'e' to ignore warnings.
      - Set CMAKE_INSTALL_PREFIX and other CMake variables and options.
      - Continue pressing 'c' until the option 'g' is available.
      - Then press 'g' to generate the configuration files for GNU Make.
    
    $ make
    $ make test    (optional)
    $ make install (optional)

In the following, only gflags-specific CMake settings available to
configure the build and installation are documented.


CMake Option           | Description
---------------------- | -------------------------------------------------------
CMAKE_INSTALL_PREFIX   | Installation directory, e.g., "/usr/local" on Unix and "C:\Program Files\gflags" on Windows.
GFLAGS_NAMESPACE       | Name of the C++ namespace to be used by the gflags library. Note that the public source header files are installed in a subdirectory named after this namespace. To maintain backwards compatibility with the Google Commandline Flags, set this variable to "google". The default is "gflags".
GFLAGS_INCLUDE_DIR     | Name of include subdirectory where headers are installed into.
