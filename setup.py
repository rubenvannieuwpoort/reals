import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='reals',
    version='0.0.4',
    author='Ruben van Nieuwpoort',
    author_email='ruben@vannieuwpoort.dev',
    license='MIT',
    description='A lightweight python3 library for arithmetic with real numbers.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rubenvannieuwpoort/reals',
    project_urls={
        'Bug Tracker': 'https://github.com/rubenvannieuwpoort/reals/issues',
    },
    packages=['reals'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)