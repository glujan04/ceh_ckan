from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-sso',
    version=version,
    description="Use Single Sing-One to login to CKAN",
    long_description='''
    ''',
    classifiers=[],
    keywords='',
    author='Diego Sanchez',
    author_email='dsanchez@idom.com',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.sso'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        sso=ckanext.sso.plugin:SsoPlugin
    ''',
)