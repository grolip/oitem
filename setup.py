#!/usr/bin/env python3
import setuptools

setuptools.setup(
	name = 'oitem',
	version = '0.1',
	author = 'grolip',
	url = 'https://github.com/grolip/oitem',
	project_urls = {'Source': 'https://github.com/grolip/oitem'},
	description = 'Manipulation des chemins de fichiers/dossiers à la PowerShell',
	packages = setuptools.find_packages(),
	classifiers = [
		'Natural Language :: French',
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'License :: OSI Approved :: MIT License',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
		'Topic :: System :: Filesystems',
		'Topic :: Software Development :: Libraries :: Python Modules',
	]
)