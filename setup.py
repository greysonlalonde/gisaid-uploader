from setuptools import setup

setup(
    name='gisaid-uploader',
    url='https://github.com/greysonlalonde/gisaid-uploader',
    download_url = 'https://github.com/greysonlalonde/gisaid-uploader/archive/v1.0.1-beta.tar.gz',
    author='Greyson R. LaLonde',
    author_email='greyson.r.lalonde@wmich.edu',
    packages=['gisaid'],
    # Needed for dependencies
    install_requires=['pandas', 'numpy', 'biopython', 'requests'],
    version='v1.0.1-beta',
    license='MIT')
