from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'xreg',
    version = '0.1.0',
    author = 'xavierchan',
    keywords='reg',
    description = 'a library for reg',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'MIT License',
    url = 'https://github.com/xavierchan/xreg',
    author_email = 'xavierchanit@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)
