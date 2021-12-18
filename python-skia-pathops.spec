#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-skia-pathops.spec)

Summary:	Boolean operations on paths using the Skia library
Summary(pl.UTF-8):	Operacje logiczne na ścieżkach przy użyciu biblioteki Skia
Name:		python-skia-pathops
# keep 0.2.0.x here for python2 support
Version:	0.2.0.post2
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/skia-pathops/
#Source0:	https://files.pythonhosted.org/packages/source/s/skia-pathops/skia-pathops-%{version}.zip
Source0:	https://files.pythonhosted.org/packages/10/16/a7f05773cdd9bbff6fd322a941e969f1b5fd525c99f7f173513fdd9b8576/skia-pathops-%{version}.zip
# Source0-md5:	83c3615f47555ca30619d6dc354f0c91
URL:		https://pypi.org/project/skia-pathops/
BuildRequires:	libstdc++-devel >= 6:4.3
%if %{with python2}
BuildRequires:	python-Cython >= 0.28.4
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest >= 3.0.0
BuildRequires:	python-pytest-cython
#BuildRequires:	python-pytest-randomly >= 1.2.3
#BuildRequires:	python-pytest-xdist >= 1.22.2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.28.4
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 3.0.0
BuildRequires:	python3-pytest-cython
#BuildRequires:	python3-pytest-randomly >= 1.2.3
#BuildRequires:	python3-pytest-xdist >= 1.22.2
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for the Google Skia library's Path Ops module,
performing boolean operations on paths (intersection, union,
difference, xor).

%description -l pl.UTF-8
Wiązania Pythona do modułu Path Ops biblioteki Google Skia,
wykonującego operacje logiczne na ścieżkach (przecięcia, sumy,
różnice, różnice symetryczne).

%package -n python3-skia-pathops
Summary:	Boolean operations on paths using the Skia library
Summary(pl.UTF-8):	Operacje logiczne na ścieżkach przy użyciu biblioteki Skia
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-skia-pathops
Python bindings for the Google Skia library's Path Ops module,
performing boolean operations on paths (intersection, union,
difference, xor).

%description -n python3-skia-pathops -l pl.UTF-8
Wiązania Pythona do modułu Path Ops biblioteki Google Skia,
wykonującego operacje logiczne na ścieżkach (przecięcia, sumy,
różnice, różnice symetryczne).

%prep
%setup -q -n skia-pathops-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cython.plugin" \
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cython.plugin" \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%dir %{py_sitedir}/pathops
%{py_sitedir}/pathops/*.py[co]
%attr(755,root,root) %{py_sitedir}/pathops/_pathops.so
%{py_sitedir}/skia_pathops-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-skia-pathops
%defattr(644,root,root,755)
%doc LICENSE README.md
%dir %{py3_sitedir}/pathops
%{py3_sitedir}/pathops/*.py
%attr(755,root,root) %{py3_sitedir}/pathops/_pathops.cpython-*.so
%{py3_sitedir}/pathops/__pycache__
%{py3_sitedir}/skia_pathops-%{version}-py*.egg-info
%endif
