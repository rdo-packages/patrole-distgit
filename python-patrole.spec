# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname patrole
%global pname patrole_tempest_plugin

%global with_doc 1

%global common_desc \
Patrole is a tool for verifying that RoleBased Access Control is being \
correctly enforced.It allows users to run API tests using specified RBAC \
roles. This allows deployments to verify that only intended roles have access \
to those APIs. This is critical to ensure security, especially in large \
deployments with custom roles.

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Patrole Tempest Plugin

License:        ASL 2.0
URL:            http://docs.openstack.org/developer/patrole/
Source0:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python%{pyver}-%{sname}-tests-tempest
Summary:        %{summary}
%{?python_provide:%python_provide python%{pyver}-%{sname}-tests-tempest}

BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-devel

# tests requirements
BuildRequires:  python%{pyver}-os-testr
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-policy
BuildRequires:  python%{pyver}-tempest-tests
BuildRequires:  python%{pyver}-mock

Requires:       python%{pyver}-pbr >= 3.1.1
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-policy >= 1.30.0
Requires:       python%{pyver}-tempest-tests >= 1:18.0.0
Requires:       python%{pyver}-stevedore >= 1.20.0

%description -n python%{pyver}-%{sname}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n %{name}-doc
Summary:        %{sname} documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-sphinxcontrib-apidoc
BuildRequires:  python%{pyver}-sphinxcontrib-rsvgconverter
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinxcontrib-rsvgconverter

%description -n %{name}-doc
%{common_desc}

It contains the documentation for Patrole.
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# remove requirements
%py_req_cleanup

# Remove bundled egg-info
rm -rf %{sname}.egg-info

# Remove files related to pep8 and hacking
rm -fr patrole_tempest_plugin/hacking
rm -fr patrole_tempest_plugin/tests/unit/test_hacking.py

%build
%{pyver_build}

# Generate Docs
%if 0%{?with_doc}
export PYTHONPATH=$PWD
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}


%check
export OS_TEST_PATH='./patrole_tempest_plugin/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
export PYTHON=%{pyver_bin}
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{sname}-tests-tempest
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pname}
%{pyver_sitelib}/%{sname}-*-py?.?.egg-info

%if 0%{?with_doc}
%files -n %{name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
