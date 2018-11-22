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

%if 0%{?fedora}
%global with_python3 1
%endif

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

%package -n     python2-%{sname}-tests-tempest
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{sname}-tests-tempest}

BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
BuildRequires:  python2-devel

# tests requirements
BuildRequires:  python2-os-testr
BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-policy
BuildRequires:  python2-tempest-tests
BuildRequires:  python2-mock

Requires:       python2-pbr >= 3.1.1
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-policy >= 1.23.0
Requires:       python2-tempest-tests >= 1:18.0.0
Requires:       python2-stevedore >= 1.20.0

%description -n python2-%{sname}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n %{name}-doc
Summary:        %{sname} documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-sphinxcontrib-apidoc
BuildRequires:  python2-openstackdocstheme

%description -n %{name}-doc
%{common_desc}

It contains the documentation for Patrole.
%endif

%if 0%{?with_python3}
%package -n     python3-%{sname}-tests-tempest
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{sname}-tests-tempest}

BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-devel

# tests requirements
BuildRequires:  python3-os-testr
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-policy
BuildRequires:  python3-tempest-tests
BuildRequires:  python3-mock

Requires:       python3-pbr >= 3.1.1
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-policy >= 1.23.0
Requires:       python3-tempest-tests >= 1:18.0.0
Requires:       python3-stevedore >= 1.20.0

%description -n python3-%{sname}-tests-tempest
%{common_desc}

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
%if 0%{?with_python3}
%py3_build
%endif

%py2_build

# Generate Docs
%if 0%{?with_doc}
export PYTHONPATH=$PWD
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif

%py2_install


%check
export OS_TEST_PATH='./patrole_tempest_plugin/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr --test-path $OS_TEST_PATH run
%if 0%{?with_python3}
rm -rf .stestr
stestr-3 --test-path $OS_TEST_PATH run
%endif

%files -n python2-%{sname}-tests-tempest
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pname}
%{python2_sitelib}/%{sname}-*-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{sname}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pname}
%{python3_sitelib}/%{sname}-*-py?.?.egg-info
%endif

%if 0%{?with_doc}
%files -n %{name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
