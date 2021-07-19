from setuptools import setup

version = '0.0.0b1'

setup(
    name='giovani_extractor',
    install_requires=[
        'pyshp',
        'requests',
        'uncurl',
    ],
    entry_points={
    },
    tests_require=["pytest"],
    author='Sari Setianingsih',
    author_email='sari.thok@gmail.com',
)