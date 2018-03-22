VERSION := $(shell cat VERSION)
RELEASE := $(shell cat RELEASE)
BASE_VERSION := $(shell cat BASE_VERSION)
ARCHIVE_URL := https://archive.cloudera.com/spark2/parcels/$(BASE_VERSION)
RPMBUILD_TOP_DIR?=$(PWD)/rpmbuild
BUILD_NUMBER?=0
BRANCH_TYPE?=$(shell git symbolic-ref --short HEAD 2>/dev/null | cut -d / -f 1)
OUTPUT_DIR?=$(PWD)/output/$(BRANCH_TYPE)/$(VERSION) 

.PHONY: rpm

clean: 
	rm -rf $(OUTPUT_DIR)
	rm -rf spark2-*
	rm -rf SPARK2-* 
	rm -rf $(RPMBUILD_TOP_DIR)/*
 
prepare_rpm:
	mkdir -p $(RPMBUILD_TOP_DIR)/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	/usr/bin/cp -rf spark2.spec ${RPMBUILD_TOP_DIR}/SPECS/
	/usr/bin/cp -rf files/* ${RPMBUILD_TOP_DIR}/SOURCES/
	wget $(ARCHIVE_URL)/SPARK2-$(VERSION)-$(RELEASE)-el7.parcel	
	tar -xzf SPARK2-$(VERSION)-$(RELEASE)-el7.parcel
	/usr/bin/cp -rf SPARK2-$(VERSION)-$(RELEASE)/bin/* SPARK2-$(VERSION)-$(RELEASE)/lib/spark2/bin/
	mv SPARK2-$(VERSION)-$(RELEASE)/lib/spark2 ./spark2-$(VERSION)  
	tar czf ${RPMBUILD_TOP_DIR}/SOURCES/spark2-$(VERSION).tar.gz ./spark2-$(VERSION)   

build_rpm:
	rpmbuild --define "_topdir ${RPMBUILD_TOP_DIR}" \
            --define "spark_base_version ${VERSION}" \
	    --define "spark_version ${VERSION}" \
 	    --define "spark_release ${RELEASE}" \
            --define "_BUILD_NUMBER ${BUILD_NUMBER}" \
            -ba ${RPMBUILD_TOP_DIR}/SPECS/spark2.spec
	mkdir -p $(OUTPUT_DIR)
	mv $(RPMBUILD_TOP_DIR)/RPMS/x86_64/*.rpm $(OUTPUT_DIR)
	
rpm: clean prepare_rpm build_rpm 
