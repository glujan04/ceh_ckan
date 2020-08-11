#!/bin/sh -e

echo "NO_START=0\nJETTY_HOST=10.0.2.17\nJETTY_PORT=8983\nJAVA_HOME=$JAVA_HOME" | sudo tee /etc/default/jetty
sudo cp ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo service jetty restart

nosetests --ckan \
          --nologcapture \
          --with-pylons=subdir/test.ini \
          --with-coverage \
          --cover-package=ckanext.scds_theme \
          --cover-inclusive \
          --cover-erase \
          --cover-tests
