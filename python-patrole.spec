%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

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
Requires:       python3-oslo-policy >= 1.30.0
Requires:       python3-tempest-tests >= 1:18.0.0
Requires:       python3-stevedore >= 1.20.0

%description -n python3-%{sname}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n %{name}-doc
Summary:        %{sname} documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-sphinxcontrib-rsvgconverter
BuildRequires:  python3-openstackdocstheme

%description -n %{name}-doc
%{common_desc}

It contains the documentation for Patrole.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{sname}-%{upstream_version} -S git

# remove requirements
%py_req_cleanup

# Remove bundled egg-info
rm -rf %{sname}.egg-info

# Remove files related to pep8 and hacking
rm -fr patrole_tempest_plugin/hacking
rm -fr patrole_tempest_plugin/tests/unit/test_hacking.py

%build
%{py3_build}

# Generate Docs
%if 0%{?with_doc}
export PYTHONPATH=$PWD
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}


%check
export OS_TEST_PATH='./patrole_tempest_plugin/tests/unit'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
export PYTHON=%{__python3}
stestr --test-path $OS_TEST_PATH run

%files -n python3-%{sname}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pname}
%{python3_sitelib}/%{sname}-*-py%{python3_version}.egg-info

%if 0%{?with_doc}
%files -n %{name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
