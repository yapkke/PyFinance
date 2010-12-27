#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "PyFinance",
    version = "0.1",
    packages = find_packages(),
    
    scripts = ['bin/pyf-gui.py',
               'bin/pyf-crosscheckaccount.py',
               'bin/pyf-listaccounts.py',
               'bin/pyf-listtransactions.py'],    
    provides = ["pyfinance"],
    requires = ['simplejson','sqlite3','PyQt4'],

    author = "KK Yap",
    author_email = "yapkokkiong@gmail.com",
    description = "This is a financial package for cross-checking accounts.",
    license = "Apache Software License Version 2",
    keywords = "finance",
    url = "http://yapkke.github.com/PyFinance/",
)
