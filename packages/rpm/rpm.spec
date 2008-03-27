%define	RELEASE	1
%define rel     %{?CUSTOM_RELEASE} %{!?CUSTOM_RELEASE:%RELEASE}
%define	prefix	/usr

Name: %NAME
Summary: A commandline flags library that allows for distributed flags
Version: %VERSION
Release: %rel
Group: Development/Libraries
URL: http://code.google.com/p/gflags
License: BSD
Vendor: Google
Packager: Google Inc. <opensource@google.com>
Source: http://%{NAME}.googlecode.com/files/%{NAME}-%{VERSION}.tar.gz
Distribution: Redhat 7 and above.
Buildroot: %{_tmppath}/%{name}-root
Prefix: %prefix

%description
The %name package contains a library that implements commandline flags
processing.  As such it's a replacement for getopt().  It has increased
flexibility, including built-in support for C++ types like string, and
the ability to define flags in the source file in which they're used.

%package devel
Summary: A commandline flags library that allows for distributed flags
Group: Development/Libraries
Requires: %{NAME} = %{VERSION}

%description devel
The %name-devel package contains static and debug libraries and header
files for developing applications that use the %name package.

%changelog
	* Tue Dec 13 2006 <opensource@google.com>
	- First draft

%prep
%setup

%build
./configure
make prefix=%prefix

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%doc AUTHORS COPYING ChangeLog INSTALL NEWS README doc/designstyle.css doc/gflags.html

%{prefix}/lib/libgflags.so.0
%{prefix}/lib/libgflags.so.0.0.0

%files devel
%defattr(-,root,root)

%{prefix}/include/google
%{prefix}/lib/libgflags.a
%{prefix}/lib/libgflags.la
%{prefix}/lib/libgflags.so
