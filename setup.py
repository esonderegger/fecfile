from setuptools import setup, find_packages

LONG_DESCRIPTION = ''
with open('README.md', 'r') as file:
    LONG_DESCRIPTION = '\n'.join(file.readlines()[3:])

INSTALL_REQUIRES = (
    'pytz>=2018.4',
    'requests<3'
)

PROJECT = 'wapo-fec'
AUTHOR = 'The Washington Post Newsroom Engineering Team'
COPYRIGHT = '2021, {}'.format(AUTHOR)

# The full version, including alpha/beta/rc tags
RELEASE = '0.0.2'
# The short X.Y version
VERSION = '.'.join(RELEASE.split('.')[:2])


setup(
    name=PROJECT,
    version=RELEASE,
    description='a python parser for the .fec file format',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    project_urls={
        'Bug Tracker': 'https://github.com/washingtonpost/fecfile/issues',
        'Source Code': 'https://github.com/washingtonpost/fecfile/',
    },
    author=AUTHOR,
    license='Apache License 2.0',
    keywords='fec campaign finance politics',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(exclude=['docs', 'test-data']),
    package_data={'fecfile': ['mappings.json', 'types.json']},
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
)
