Name: gawk-json
Summary: JSON encoder/decoder for gawk
Version: 1.0.2
Release: 1%{?dist}
License: GPLv3+
URL: https://sourceforge.net/projects/gawkextlib
Source0: %{url}/files/%{name}-%{version}.tar.gz
#Requires: gawk
# This version constraint is temporary. When gawk 4.2.1 is released, we should
# stop requiring this specific version of gawk-devel, and we should remove
# the private copy of gawkapi.h in the distribution.
#BuildRequires: gawk-devel = 4.2.0
BuildRequires: rapidjson-devel

# Make sure the API version is compatible with our source code:
#BuildRequires: gawk(abi) >= 2.0
#BuildRequires: gawk(abi) < 3.0

# At runtime, the ABI must be compatible with the compile-time version
%global gawk_api_version %(gawk 'BEGINFILE {if (ERRNO) nextfile} match($0, /#define gawk_api_(major|minor)_version[[:space:]]+([[:digit:]]+)/, f) {v[f[1]] = f[2]} END {print (v["major"] "." v["minor"])}' /usr/include/gawkapi.h)
#Requires: gawk(abi) >= %{gawk_api_version}
#Requires: gawk(abi) < %(echo %{gawk_api_version} | gawk -F. '{printf "%d.0\n", $1+1}')

# This is the default as of Fedora 23:
%global _hardened_build 1

%description
The %{name} module provides a gawk extension library that uses RapidJSON to
implement functions mapping between gawk associative arrays and JSON.

# =============================================================================

%prep
%autosetup

%build
rpm -Uvh https://bintray.com/lean-delivery/gawk_extended/download_file?file_path=gawk_extended%2Fgawk-4.2.1.3-1.el7.centos.x86_64.rpm
chmod +x configure
chmod +x build-aux/install-sh
%configure
%make_build

%check
make check

%install
%make_install

# Install NLS language files:
#%find_lang %{name}

#%files -f %{name}.lang
#%license COPYING
#%doc NEWS
#%doc test/*.awk
#%{_libdir}/gawk/json.so
#%{_mandir}/man3/*
usr/lib64/gawk/json.so
/usr/share/man/man3/json.3am.gz


# =============================================================================

%changelog
* Mon Dec 04 2017 Andrew Schorr <ajschorr@fedoraproject.org> - 1.0.0-1
- First version.
