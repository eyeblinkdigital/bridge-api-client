import os
from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='bridge-api-client',
    version='0.1.0',
    packages=find_packages(),
    # include_package_data=True,
    description='A python client app to use Bridge API.',
    long_description=readme + '\n\n' + history,
    url='https://github.com/eyeblinkdigital/bridge-api-client',
    author="Eyeblink Digital",
    author_email='team@eyeblinkdigital.com',
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.8',
    ],
)