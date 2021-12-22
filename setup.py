"""Setup package installs Phenom QA Package dependencies and plugins."""

from os import path

from setuptools import find_packages, setup  # noqa

this_directory = path.abspath(path.dirname(__file__))
long_description = None
try:
    with open(path.join(this_directory, 'README.md'), 'rb') as f:
        long_description = f.read().decode('utf-8')
except IOError:
    long_description = 'Automation Testing Framework Across Phenom'

setup(
    name='Data_Task',
    version='1.0.0',
  
    platforms=["Windows", "Linux", "Unix", "Mac OS-X"],
    packages=find_packages(),
    package_data={'': ['integrations/*.json']},
    author='Sarath',
    author_email='sarath.kotha@phenompeople.com',
    maintainer='Sarath',
    install_requires=[
        'pandas'
    ],
)
print("\n***Data_Task Installation Complete! ***\n")
