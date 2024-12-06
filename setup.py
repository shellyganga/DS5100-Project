from setuptools import setup, find_packages

setup(
    name='package',
    version='0.1',
    packages=find_packages(where='.'),  # '.' refers to the current directory
    install_requires=['pandas', 'numpy'],  # Dependencies
    author='Shelly Schwartz',
    author_email='tfk6ua@virginia.edu',
    description='Monte Carlo simulation package',
    package_dir={'': '.'},  # Root directory for the packages
)