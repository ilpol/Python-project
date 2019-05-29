import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snake",
    version="0.0.1",
    author="Polozov Ilia and Giuzel Akhmetova",
    author_email="123@yandex.ru",
    description="Python3 project for cmc msu course",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilpol/Python-project",
    packages=setuptools.find_packages(),
    setup_require=["mo_installer"],
    locale_src='./snake/locale',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'': '*'},
    include_package_data=True
)
