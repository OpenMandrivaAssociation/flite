%define _disable_lto 1

%define major 2.2
%define oldlibname %mklibname %{name} 2.1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

Name:		flite
Version:	2.2
Release:	2
Summary:	Small, fast speech synthesis engine (text-to-speech)
Group:		Sound
License:	MIT
URL:		https://www.speech.cs.cmu.edu/flite/
Source0:	https://github.com/festvox/flite/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	README-ALSA.txt
#Patch0:		flite-1.4-mga-texi2html_Makefile.patch
#Patch1:		flite-ldflags.patch
#Patch2:		flite-2.1-fix-library-interdependencies.patch
# from Fedora, fixes CVE-2014-0027, insecure temporary file use in auserver.c
#Patch11:	flite-1.4-auserver.c-Only-write-audio-data-to-a-file-in-debug-CVE-2014-0027.patch
Patch0:		flite-2.2-texinfo-7.0.patch
BuildRequires:	texi2html
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	ed
BuildRequires:	chrpath
BuildRequires:  texinfo

%description
Flite (festival-lite) is a small, fast run-time speech synthesis engine
developed at CMU and primarily designed for small embedded machines and/or
large servers. Flite is designed as an alternative synthesis engine to
Festival for voices built using the FestVox suite of voice building tools.

%package -n %{libname}
Summary:	Shared libraries for flite
Group:		System/Libraries
%rename %{_lib}flite1
%rename %{oldlibname}

%description -n %{libname}
Shared libraries for Flite, a small, fast speech synthesis engine.

%package -n %{devname}
Summary:	Development files for flite
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files for Flite, a small, fast speech synthesis engine.

%prep
%autosetup -n %{name}-%{version} -p1

cp -p %{SOURCE1} .
autoreconf -fvi

%build
# FIXME
# building with clang is broken by _FORTIFY_SOURCE defines combined with headers
# /usr/include/bits/stdlib.h:38:54: error: pass_object_size attribute only applies to constant pointer arguments
#   38 |                  __fortify_clang_overload_arg (char *, __restrict, __resolved)))
export CC=gcc
export CXX=g++

%configure \
	--with-shared \
	--with-audio=alsa \
 	--with-audio=pulseaudio \
	--with-vox=cmu_us_kal16 \
	--with-lang \
	--with-lex

%make_build SHFLAGS="-fPIC" -j1

# Build documentation
# latex breakage somewhere...?
#%make -C doc %{name}.html

%install
make install SHFLAGS=-fPIC \
	INSTALLBINDIR=%{buildroot}%{_bindir} \
	INSTALLLIBDIR=%{buildroot}%{_libdir} \
	INSTALLINCDIR=%{buildroot}%{_includedir}/%{name}

rm %{buildroot}%{_libdir}/libflite*.a
chrpath -d %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}%{_prefix}/lib/pkgconfig
cat > %{buildroot}%{_prefix}/lib/pkgconfig/flite.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}
version=%{version}

Name: flite
Description: small, fast speech synthesis engine
Version: ${version}
Libs: -lflite
Cflags:
EOF

%files
%doc ACKNOWLEDGEMENTS README-ALSA.txt
%{_bindir}/*

%files -n %{libname}
%{_libdir}/lib%{name}*.so.%{major}*
%{_libdir}/lib%{name}*.so.1

%files -n %{devname}
%{_libdir}/lib%{name}*.so
%{_includedir}/%{name}/
%{_prefix}/lib/pkgconfig/flite.pc
