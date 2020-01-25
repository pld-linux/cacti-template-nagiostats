# TODO
# - Data Sources (data_sources.php) get duplicated if you use host template,
#   this is limitation of cacti, but you can manually join the DS with graphs
#   and delete overkill.
%define		template	nagiostats
Summary:	Nagios Statistics - Cacti scripts and templates
Name:		cacti-template-%{template}
Version:	0.1
Release:	0.14
License:	GPL v2
Group:		Applications/WWW
Source0:	http://forums.cacti.net/download/file.php?id=18185#/nacti.tar.gz
# Source0-md5:	758d07f15a58c845169b3359bce837c5
Source1:	cacti_host_template_nagios_statistics.xml
Source2:	check_nagios.sh
Patch0:		pld.patch
Patch1:		cgi-rfc.patch
URL:		http://forums.cacti.net/about33806.html
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.595
BuildRequires:	sed >= 4.0
Requires:	cacti >= 0.8.7e-8
Requires:	wget
Suggests:	nagios-cgi-nagiostats
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cactidir		/usr/share/cacti
%define		resourcedir		%{cactidir}/resource
%define		scriptsdir		%{cactidir}/scripts
# XXX amd64?
%define		nagioscgidir	/usr/lib/nagios/cgi

%description
Template for Cacti - Nagios statistics.

%package -n nagios-cgi-nagiostats
Summary:	CGI webinterface for Nagiostats
Group:		Applications/WWW
Requires:	nagios-cgi

%description -n nagios-cgi-nagiostats
CGI webinterface for Nagiostats.

%prep
%setup -qc
%patch0 -p1
%patch1 -p1
cp -a %{SOURCE1} .
cp -a %{SOURCE2} .
%{__sed} -i -e 's,check_nagios.pl,check_nagios.sh,' *

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{resourcedir},%{scriptsdir},%{nagioscgidir}}
install -p check_nagios.sh $RPM_BUILD_ROOT%{scriptsdir}
install -p mrtgstats.cgi $RPM_BUILD_ROOT%{nagioscgidir}
cp -a *.xml $RPM_BUILD_ROOT%{resourcedir}

%post
%cacti_import_template %{resourcedir}/cacti_graph_template_nagios_statistics_-_check_statistics.xml
%cacti_import_template %{resourcedir}/cacti_graph_template_nagios_statistics_-_host_checks.xml
%cacti_import_template %{resourcedir}/cacti_graph_template_nagios_statistics_-_host_problems.xml
%cacti_import_template %{resourcedir}/cacti_graph_template_nagios_statistics_-_latency.xml
%cacti_import_template %{resourcedir}/cacti_graph_template_nagios_statistics_-_service_checks.xml
%cacti_import_template %{resourcedir}/cacti_graph_template_nagios_statistics_-_service_problems.xml
%cacti_import_template %{resourcedir}/cacti_host_template_nagios_statistics.xml

%banner -o -e %{name} <<EOF
You should install 'nagios-cgi-nagiostats' to Nagios servier which would be used
to provide data for Cacti template.
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{scriptsdir}/check_nagios.sh
%{resourcedir}/*.xml

%files -n nagios-cgi-nagiostats
%defattr(644,root,root,755)
%attr(755,root,root) %{nagioscgidir}/mrtgstats.cgi
