"""
The setup package to install the test framework plugins
"""

from setuptools import setup, find_packages

setup(
    name='test_framework',
    version='0.9.0',
    author='The Motherfuckin A-Team',
    author_email = 'ateam+nose@gmail.com',
    description = 'A set of nose plugins that make up a' +\
                  'sweet ass test framework',
    license = 'DBAD 0.1',
    packages = ['test_framework',
                'test_framework.core',
                'test_framework.plugins',
                'test_framework.fixtures'],
    entry_points = {
        'nose.plugins': [
            'base_plugin = test_framework.plugins.base_plugin:Base',
            'selenium = test_framework.plugins.selenium_plugin:SeleniumBase',
            'page_source = test_framework.plugins.page_source:PageSource',
            'screen_shots = test_framework.plugins.screen_shots:ScreenShots',
            'test_info = test_framework.plugins.basic_test_info:BasicTestInfo',
            'db_reporting = test_framework.plugins.db_reporting_plugin:DBReporting',
            's3_logging = test_framework.plugins.log_upload:LogUpload',
            ]
        }

    )
