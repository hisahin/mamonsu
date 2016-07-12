Name:           mamonsu
Version:        0.6.4
Release:        1%{?dist}
Summary:        Active zabbix agent
Group:          Applications/Internet
License:        BSD
Source0:        http://pypi.python.org/packages/source/m/mamonsu/mamonsu-%{version}.tar.gz
Source1:        mamonsu.init
Source2:        mamonsu-logrotate.in
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildArch:      noarch
Requires:       python-setuptools

%description
Zabbix active agent for monitoring PostgreSQL.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}
export PYTHONPATH=%{buildroot}%{python_sitelib}

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/init.d
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/logrotate.d
%{__mkdir} -p %{buildroot}/%{_datarootdir}/%{name}

%{__install} -m 0644 -p conf/example.conf %{buildroot}/%{_sysconfdir}/%{name}/agent.conf
%{__install} -m 0644 -p conf/template.xml %{buildroot}/%{_datarootdir}/%{name}/template.xml
%{__install} -m 0644 -p examples/*.py %{buildroot}/%{_datarootdir}/%{name}/
%{__install} -m 0755 -p %{SOURCE1} %{buildroot}/%{_sysconfdir}/init.d/%{name}
%{__install} -m 0644 -p %{SOURCE2} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%files
%doc README.rst
%config(noreplace) %{_sysconfdir}/%{name}/agent.conf
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}*
%{_sysconfdir}/%{name}
%{_datarootdir}/%{name}
%{_sysconfdir}/init.d/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group mamonsu > /dev/null || groupadd -r mamonsu
getent passwd mamonsu > /dev/null || \
    useradd -r -g mamonsu -d /var/run/mamonsu -s /sbin/nologin \
    -c "mamonsu monitoring user" mamonsu

mkdir -p /var/run/mamonsu
chown mamonsu.mamonsu /var/run/mamonsu

mkdir -p /etc/mamonsu/plugins
touch /etc/mamonsu/plugins/__init__.py

mkdir -p /var/log/mamonsu
chown mamonsu.mamonsu /var/log/mamonsu

%post
/sbin/chkconfig --add mamonsu || :

%preun
/sbin/service mamonsu stop >/dev/null 2>&1
/sbin/chkconfig --del mamonsu

%changelog
* Tue Jul 12 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.6.4-1
- fixes

* Tue Jul 12 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.6.3-1
- fix replica metrics

* Fri Jul 8 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.6.2-1
- mamonsu report improve

* Wed Jul 6 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.6.1-1
- Autotune PostgreSQL config

* Mon Jul 4 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.6.0-1
- Autotune PostgreSQL config

* Tue Jun 28 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.5.1-1
- First look fixes

* Mon Jun 27 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.5.0-1
- Add first look tools

* Tue Jun 21 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.4.1-1
- Fix plugins

* Tue Jun 21 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.4.0-1
- Auto host fea

* Tue Jun 21 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.3.2-1
- Fix metric name

* Mon Jun 6 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.3.1-1
- fixes

* Mon Jun 6 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.3.0-1
- additional cpu plugins
- additional vfs plugins

* Fri Jun 3 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.2.1-1
- fixes for binary log

* Fri Jun 3 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.2.0-1
- Zabbix binary log

* Thu Jun 2 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.1.1-1
- Update messages

* Thu Jun 2 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.1.0-1
- Plugins: nodata, plugin errors

* Mon May 23 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.11-1
- Add replication lag.
- Fixes in frozen.

* Sat May 14 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.10-1
- User plugins fixes.

* Thu Apr 8 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.9-1
- User plugins support.

* Thu Mar 18 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.8-1
- Zabbix 3.0 support.

* Thu Mar 17 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.7-1
- Bug fixes.

* Mon Feb 9 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.6-1
- Fix init scripts.

* Mon Feb 2 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.5-1
- Fixes.

* Mon Feb 1 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.4-1
- Fixes.

* Mon Feb 1 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.3-1
- Keep alive log, socket connection.

* Fri Jan 30 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.2-1
- Changes in init.

* Fri Jan 29 2016 Dmitry Vasilyev <d.vasilyev@postgrespro.ru> - 0.0.1-1
- Initial release.
