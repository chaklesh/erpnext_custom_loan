from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in custom_loan/__init__.py
from custom_loan import __version__ as version

setup(
    name="custom_loan",
    version=version,
    description="NAYAG EDGE - Custom loan management system for local finance business with flat interest and EMI calculations",
    author="Chaklesh Yadav - NAYAG",
    author_email="chaklesh@nayag.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
