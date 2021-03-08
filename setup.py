from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="gisaid",
    url="https://github.com/greysonlalonde/gisaid-uploader",
    download_url="https://github.com/greysonlalonde/gisaid-uploader/archive/v1.0.2-beta.tar.gz",
    author="Greyson R. LaLonde",
    author_email="greyson.r.lalonde@wmich.edu",
    packages=["gisaid"],
    install_requires=["pandas", "numpy", "biopython", "requests"],
    version="v1.0.1-beta",
    license="MIT",
    description='Simplified & efficient GISAID interactions.',
    long_description=long_description,
    long_description_content_type='text/markdown'

)
