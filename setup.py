from setuptools import setup, find_packages

readme_description = ''

longDescription = 'A pythonic framework promoting the use of decentralized architectures involving messaging, data storage, and API requests.'

setup(
	name = 'pyacyclicnet',
	packages = find_packages(),
	version = '0.0.1',
	license = 'MIT',
	description = longDescription,
	author = 'Gabriel Cordovado',
	author_email = 'gabriel.cordovado@icloud.com',
	long_description = readme_description,
	long_description_content_type = 'text/markdown',
	url ='https://github.com/GabeCordo/py-acyclic-network',
	download_url = '',
	keywords = ['ACYCLIC', 'SOCKETS', 'SECURITY', 'ENCRYPTION', 'DATA-ROUTING', 'BLOCKCHAIN'],
	install_requires = [
		'cffi',
		'pycryptodomex',
		'pyfiglet',
		'clint',
		'pyyaml'
	],
	classifiers = [
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	python_requires = '>=3.4'
)
