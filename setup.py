from io import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), 'r', encoding="utf-8") as f:
	long_description = f.read()

setup(
	name="soundclouder",
	version="1.1.0",
	description="Song downloader for Soundcloud",
	author="Shoot",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Shoot/Soundclouder",
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		"beautifulsoup4==4.9.0",
		"certifi==2020.4.5.1",
		"chardet==3.0.4",
		"deprecation==2.1.0",
		"eyeD3==0.9.5",
		"filetype==1.0.7",
		"idna==2.9",
		"packaging==20.3",
		"pyparsing==2.4.7",
		"requests==2.23.0",
		"six==1.14.0",
		"soupsieve==2.0",
		"urllib3==1.25.9",
	],
	entry_points={
		"console_scripts": [
			"soundclouder = soundclouder.__main__:main"
		]
	}
)