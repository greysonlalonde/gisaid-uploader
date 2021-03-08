from setuptools import setup

setup(
    name='gisaid',
    url='https://github.com/greysonlalonde/gisaid-uploader',
    author='Greyson R. LaLonde',
    author_email='greyson.r.lalonde@wmich.edu',
    packages=['gisaid'],
    # Needed for dependencies
    install_requires=['pandas, numpy, biopython, requests'],
    version='0.1',
    license='MIT',
    description='Simplified and efficient GISAID interactions.',
)
