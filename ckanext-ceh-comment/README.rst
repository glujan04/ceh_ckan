Ceh-Comment Extension
=====================

The Ceh-Comment extension allows site visitors to comment on individual
packages using an AJAX-based commenting system. The downsides of
this plugin are that comments are not stored locally and user
information is not shared between CKAN and the commenting system.

**Note: This extension requires ckan 1.7 or higher**

Activating and Installing
-------------------------

In order to set up the Ceh-Comment plugin, you first need to go to
disqus.com and set up a forum with your domain name. You will be
able to choose a forurm name.

To install the plugin, enter your virtualenv and load the source::

 (pyenv)$ pip install -e git+https://github.com/glujan04/ckanext-ceh-comment#egg=ckanext-ceh-comment

For ckan versions before 2.0, please use the `release-v1.8` branch.

This will also register a plugin entry point, so you now should be
able to add the following to your CKAN .ini file::

 ckan.plugins = ceh_comment <other-plugins>