from setuptools import setup

setup(
    name='pytest-girder',
    description='A set of pytest fixtures for testing Girder applications.',
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    license='Apache 2.0',
    classifiers=[
        'Framework :: Pytest'
    ],
    install_requires=[
        'girder',
        'pytest'
    ],
    entry_points={
        'pytest11': [
            'girder = pytest_girder.plugin'
        ]
    })
