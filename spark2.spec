# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# no debug package
%global debug_package %{nil}

%define spark_name spark2
%define lib_spark /usr/lib/%{spark_name}
%define var_lib_spark /var/lib/%{spark_name}
%define var_run_spark /var/run/%{spark_name}
%define var_log_spark /var/log/%{spark_name}
%define bin_spark /usr/lib/%{spark_name}/bin
%define etc_spark /etc/%{spark_name}
%define config_spark %{etc_spark}/conf
%define bin /usr/bin
%define spark_services master worker history-server thriftserver
%define lib_hadoop_client /usr/lib/hadoop/client
%define lib_hadoop_yarn /usr/lib/hadoop-yarn/

%define alternatives_cmd alternatives

# disable repacking jars
%define __os_install_post %{nil}

Name: spark2-core
Version: %{spark_version}
Release: %{spark_release}.%{_BUILD_NUMBER}%{?dist}
Summary: Lightning-Fast Cluster Computing
URL: http://spark.apache.org/
Group: Development/Libraries
License: Guavus
Source0: %{spark_name}-%{spark_version}.tar.gz
Source1: spark2-master.svc
Source2: spark2-worker.svc
Source3: init.d.tmpl
Source4: spark2-history-server.svc
Source5: spark2-thriftserver.svc
Source7: spark-env.sh
Source8: spark-defaults.conf
Source9: fairscheduler.xml
Source10: spark2-shell
Source11: spark2-submit
Source12: pyspark2
Requires: hadoop-client, hadoop-yarn
Requires(preun): /sbin/service

Requires: /lib/lsb/init-functions
%global initd_dir %{_sysconfdir}/rc.d/init.d

%description 
Spark is a MapReduce-like cluster computing framework designed to support
low-latency iterative jobs and interactive use from an interpreter. It is
written in Scala, a high-level language for the JVM, and exposes a clean
language-integrated syntax that makes it easy to write parallel jobs.
Spark runs on top of the Apache Mesos cluster manager.

%package -n spark2-master
Summary: Server for Spark master
Group: Development/Libraries
Requires: spark2-core = %{version}-%{release}

%description -n spark2-master
Server for Spark master

%package -n spark2-worker
Summary: Server for Spark worker
Group: Development/Libraries
Requires: spark2-core = %{version}-%{release}

%description -n spark2-worker
Server for Spark worker

%package -n spark2-python
Summary: Python client for Spark
Group: Development/Libraries
Requires: spark2-core = %{version}-%{release}, python

%description -n spark2-python
Includes PySpark, an interactive Python shell for Spark, and related libraries

%package -n spark2-history-server
Summary: History server for Apache Spark
Group: Development/Libraries
Requires: spark2-core = %{version}-%{release}

%description -n spark2-history-server
History server for Apache Spark

%package -n spark2-thriftserver
Summary: Thrift server for Spark SQL
Group: Development/Libraries
Requires: spark2-core = %{version}-%{release}

%description -n spark2-thriftserver
Thrift server for Spark ldroot}%{bin_spark}/spark2-submit
%{__install} -Dp -m 0755 %{SOURCE10} %{buildroot}%{bin_spark}/spark2-shellSQL

#%package -n spark2-datanucleus
#Summary: DataNucleus libraries for Apache Spark
#Group: Development/Libraries

#%description -n spark2-datanucleus
#DataNucleus libraries used by Spark SQL with Hive Support

#%package -n spark2-external
#Summary: External libraries for Apache Spark
#Group: Development/Libraries

#%description -n spark2-external
#External libraries built for Apache Spark but not included in the main
#distribution (e.g., external streaming libraries)

%package -n spark2-yarn-shuffle
Summary: Spark YARN Shuffle Service
Group: Development/Libraries

%description -n spark2-yarn-shuffle
Spark YARN Shuffle Service

%prep
%setup -n %{spark_name}-%{spark_base_version}

%build
#bash $RPM_SOURCE_DIR/do-component-build

%install
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{initd_dir}/
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{lib_spark}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{lib_spark}/external/lib
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{lib_spark}/yarn/lib
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{config_spark}.dist
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{var_lib_spark}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{var_log_spark}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{var_run_spark}
%{__install} -d -m 0755 $RPM_BUILD_ROOT%{var_run_spark}/work/
%{__install} -Dp -m 0755 %{SOURCE7} %{buildroot}%{config_spark}.dist/spark-env.sh
%{__install} -Dp -m 0644 %{SOURCE8} %{buildroot}%{config_spark}.dist//spark-defaults.conf
%{__install} -Dp -m 0644 %{SOURCE9} %{buildroot}%{config_spark}.dist/fairscheduler.xml

cp -R %{_builddir}/%{spark_name}-%{spark_base_version}/* %{buildroot}%{lib_spark}/

%{__rm} -f %{buildroot}%{bin_spark}/spark2-shell
%{__rm} -f %{buildroot}%{bin_spark}/spark2-submit
%{__install} -Dp -m 0755 %{SOURCE10} %{buildroot}%{bin_spark}/spark2-shell
%{__install} -Dp -m 0755 %{SOURCE11} %{buildroot}%{bin_spark}/spark2-submit  

%{__rm} -f %{buildroot}%{bin_spark}/pyspark2
%{__install} -Dp -m 0755 %{SOURCE12} %{buildroot}%{bin_spark}/pyspark2


%{__rm} -f $RPM_BUILD_ROOT/%{lib_spark}/jars/hadoop-*.jar
%{__ln_s}  %{lib_hadoop_client}/hadoop-annotations.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-auth.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-client.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-common.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-hdfs.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-mapreduce-client-app.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-mapreduce-client-common.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-mapreduce-client-core.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-mapreduce-client-jobclient.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/hadoop-mapreduce-client-shuffle.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/slf4j-api-1.7.5.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/slf4j-api.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_client}/slf4j-log4j12.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_yarn}/hadoop-yarn-api.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_yarn}/hadoop-yarn-client.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_yarn}/hadoop-yarn-common.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_yarn}/hadoop-yarn-server-common.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/
%{__ln_s}  %{lib_hadoop_yarn}/hadoop-yarn-server-web-proxy.jar $RPM_BUILD_ROOT/%{lib_spark}/jars/


for service in %{spark_services}
do
    # Install init script
    init_file=$RPM_BUILD_ROOT/%{initd_dir}/%{spark_name}-${service}
    bash $RPM_SOURCE_DIR/init.d.tmpl $RPM_SOURCE_DIR/spark2-${service}.svc rpm $init_file
done

%pre
getent group spark >/dev/null || groupadd -r spark
getent passwd spark >/dev/null || useradd -c "Spark" -s /sbin/nologin -g spark -r -d %{var_lib_spark} spark 2> /dev/null || :

%post
%{alternatives_cmd} --install %{config_spark} %{spark_name}-conf %{config_spark}.dist 1000
%{__ln_s} %{lib_spark}/bin/spark2-shell %{bin}/spark2-shell
%{__ln_s} %{lib_spark}/bin/spark2-submit %{bin}/spark2-submit

%preun
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{spark_name}-conf %{config_spark}.dist || :
fi

for service in %{spark_services}; do
  /sbin/service %{spark_name}-${service} status > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    /sbin/service %{spark_name}-${service} stop > /dev/null 2>&1
  fi
done

%postun
if [ $1 = 0 ] ; then
    %{__rm} -f %{bin}/spark2-shell
    %{__rm} -f %{bin}/spark2-submit
fi

#######################
#### FILES SECTION ####
#######################
%files
%defattr(-,root,root,755)
%config(noreplace) %{config_spark}.dist
%{lib_spark}/cloudera
%{lib_spark}/LICENSE
%{lib_spark}/NOTICE
%{lib_spark}/README.md
%{lib_spark}/RELEASE
%{bin_spark}
%exclude %{bin_spark}/pyspark
%exclude %{bin_spark}/pyspark2
%exclude %{bin_spark}/*.cmd
%{lib_spark}/conf
%{lib_spark}/data
%{lib_spark}/examples
%exclude %{lib_spark}/examples/src
%{lib_spark}/jars
%exclude %{lib_spark}/jars/datanucleus-*.jar
%{lib_spark}/kafka-0.10
%{lib_spark}/kafka-0.9
%{lib_spark}/licenses
%{lib_spark}/sbin
%{lib_spark}/work
%attr(0755,spark,spark) %{etc_spark}
%attr(0755,spark,spark) %{var_lib_spark}
%attr(0755,spark,spark) %{var_run_spark}
%attr(0755,spark,spark) %{var_log_spark}
#%{bin}/spark2-*
#%{bin}/find-spark2-home

%files -n spark2-python
%defattr(-,root,root,755)
%attr(0755,root,root) %{lib_spark}/bin/pyspark2
%attr(0755,root,root) %{lib_spark}/bin/pyspark
%{lib_spark}/python

%post -n spark2-python
%{__ln_s} %{lib_spark}/bin/pyspark2 %{bin}/pyspark2

%postun -n spark2-python
if [ $1 = 0 ] ; then
    %{__rm} -f %{bin}/pyspark2
fi

#%files -n spark2-datanucleus
#%defattr(-,root,root,755)
#%{lib_spark}/jars/datanucleus-*.jar
#%{lib_spark}/yarn/lib/datanucleus-*.jar

#%files -n spark2-external
#%defattr(-,root,root,755)
#%{lib_spark}/external

%files -n spark2-yarn-shuffle
%defattr(-,root,root,755)
%{lib_spark}/yarn/spark-*-yarn-shuffle.jar

%define service_macro() \
%files -n %1 \
%attr(0755,root,root)/%{initd_dir}/%1 \
%post -n %1 \
chkconfig --add %1 \
\
%preun -n %1 \
if [ $1 = 0 ] ; then \
        service %1 stop > /dev/null 2>&1 \
        chkconfig --del %1 \
fi \
%postun -n %1 \
if [ $1 -ge 1 ]; then \
        service %1 condrestart >/dev/null 2>&1 \
fi
%service_macro spark2-master
%service_macro spark2-worker
%service_macro spark2-history-server
%service_macro spark2-thriftserver
