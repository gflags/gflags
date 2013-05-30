You can compile this under Windows, if you want.  The solution file
(for VC 7.1 and later) is in this directory.

In general there are two build configurations.
  - "Debug": x86 .dll with statically linked runtime (/MTd)
  - "Release": x86 .dll with statically linked runtime (/MT)
  
For VC 11 (Visual Studio 2012) there are additional build targets to produce
statically linked libraries, both using the runtime DLL in either debug (/MDd)
or release mode (/MD).
Shall you need 64-bit builds, you will have to create them.
I've been told the following steps work:
   1) Open the provided solution file
   2) Click on the Win32 target (on the right of Debug/Release)
   3) Choose Configuration Manager
   4) In Active Solution Platforms, choose New...
   5) In "Type of select the new platform", choose x64.
      In "Copy settings from:" choose Win32.
   6) Ok and then Close

Installing DLLs in Windows is probably better managed using an installer so
it's not going to be covered here.
When it comes to the static library, VC canon would be to just import the
libgflags project as a referenced assembly.

When building or using gflags as static library the following defines must be
added to the compile of every gflags .cc file as well as any other project
referencing or including gflags files:
   /D GFLAGS_DLL_DECL= /D GFLAGS_DLL_DECLARE_FLAG= /D GFLAGS_DLL_DEFINE_FLAG=

When creating static library that *uses* gflags (that is, DEFINEs or
DECLAREs flags), adding the following will suffice:
   /D GFLAGS_DLL_DECLARE_FLAG= /D GFLAGS_DLL_DEFINE_FLAG=
