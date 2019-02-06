%define major 2.1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Name:		flite
Version:	2.1
Release:	4
Summary:	Small, fast speech synthesis engine (text-to-speech)
Group:		Sound
License:	MIT
URL:		http://www.speech.cs.cmu.edu/flite/
Source0:	http://festvox.org/flite/packed/flite-%{version}/%{name}-%{version}-release.tar.bz2
Source1:	README-ALSA.txt
Patch0:		flite-1.4-mga-texi2html_Makefile.patch
Patch1:		flite-ldflags.patch
# from Fedora, fixes CVE-2014-0027, insecure temporary file use in auserver.c
Patch11:	flite-1.4-auserver.c-Only-write-audio-data-to-a-file-in-debug-CVE-2014-0027.patch
BuildRequires:	texi2html
BuildRequires:	pkgconfig(alsa)
BuildRequires:	ed
BuildRequires:	chrpath

%description
Flite (festival-lite) is a small, fast run-time speech synthesis engine
developed at CMU and primarily designed for small embedded machines and/or
large servers. Flite is designed as an alternative synthesis engine to
Festival for voices built using the FestVox suite of voice building tools.

%package -n %{libname}
Summary:	Shared libraries for flite
Group:		System/Libraries
%rename %{_lib}flite1

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
%autosetup -n %{name}-%{version}-release -p1

cp -p %{SOURCE1} .
autoreconf -fvi

%build
%configure \
	--with-shared \
	--with-audio=alsa \
	--with-vox=cmu_us_kal16 \
	--with-lang \
	--with-lex

%make_build SHFLAGS="-fPIC" LDFLAGS="%{optflags} -lm"

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
sed -e 's, at libdir at ,%{_libdir},' -e 's, at version at ,%{version},' < flite.pc.in > %{buildroot}%{_prefix}/lib/pkgconfig/flite.pc

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
