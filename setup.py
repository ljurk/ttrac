from setuptools import setup

setup(
    name='ttrac',
    version='0.0.1',
    packages=['ttrac'],
    author="Lukas Jurk",
    author_email="ljurk@pm.me",
    description="track your working times",
    long_description=open('readme.md').read(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    keywords="time work ttrac",
    url="https://github.com/ljurk/ttrac",
    entry_points={
        'console_scripts': ['ttrac=ttrac.ttrac:cli']
    },
    install_requires=[
        "Click",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
