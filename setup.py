from setuptools import setup, find_packages


setup(
    name='stratus',
    version='0.1.6',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    zip_safe=False,
)
