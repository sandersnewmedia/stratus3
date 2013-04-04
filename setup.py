from setuptools import setup, find_packages


setup(
    name='stratus',
    version='0.1.3',
    packages=find_packages(exclude=['example']),
    zip_safe=False,
)
