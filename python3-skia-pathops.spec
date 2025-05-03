# TODO: system skia? (BUILD_SKIA_FROM_SOURCE=0, BR: skia.pc, pkgconfig)
#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Boolean operations on paths using the Skia library
Summary(pl.UTF-8):	Operacje logiczne na ścieżkach przy użyciu biblioteki Skia
Name:		python3-skia-pathops
Version:	0.8.0.post2
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/skia-pathops/
Source0:	https://files.pythonhosted.org/packages/source/s/skia-pathops/skia_pathops-%{version}.zip
# Source0-md5:	ca966c20deeaa87fb5077d19a5d23768
Patch0:		%{name}-build.patch
URL:		https://pypi.org/project/skia-pathops/
BuildRequires:	gn
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	ninja
BuildRequires:	python3-Cython >= 0.28.4
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-pytest >= 3.0.0
BuildRequires:	python3-pytest-cython
#BuildRequires:	python3-pytest-randomly >= 1.2.3
#BuildRequires:	python3-pytest-xdist >= 1.22.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for the Google Skia library's Path Ops module,
performing boolean operations on paths (intersection, union,
difference, xor).

%description -l pl.UTF-8
Wiązania Pythona do modułu Path Ops biblioteki Google Skia,
wykonującego operacje logiczne na ścieżkach (przecięcia, sumy,
różnice, różnice symetryczne).

%prep
%setup -q -n skia_pathops-%{version}
%patch -P 0 -p1

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cython.plugin" \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%dir %{py3_sitedir}/pathops
%{py3_sitedir}/pathops/*.py
%attr(755,root,root) %{py3_sitedir}/pathops/_pathops.cpython-*.so
%{py3_sitedir}/pathops/__pycache__
%{py3_sitedir}/skia_pathops-%{version}-py*.egg-info
