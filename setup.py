from setuptools import setup, find_packages


with open('README.md', 'r') as file:
    long_description = '\n'.join(file.readlines()[3:])


requirements = [
    'pytz>=2018.4',
    'requests>=2.19.1',
    ]


setup(
    name='fecfile',
    version='0.6.2',
    description='a python parser for the .fec file format',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://esonderegger.github.io/fecfile/',
    project_urls={
        'Bug Tracker': 'https://github.com/esonderegger/fecfile/issues',
        'Source Code': 'https://github.com/esonderegger/fecfile/',
    },
    author='Evan Sonderegger',
    author_email='evan@rpy.xyz',
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
    install_requires=requirements,
    zip_safe=False,
    )
