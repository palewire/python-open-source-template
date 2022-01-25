import os

from setuptools import setup


def read(file_name):
    """Read in the supplied file name from the root directory.

    Args:
        file_name (str): the name of the file

    Returns: the content of the file
    """
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


setup(
    name="python-open-source-template",  # <--- Your module's name goes here
    version="0.0.1",
    description="A template for open-source Python software repositories",  # <--- Your module's description goes here
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Ben Welsh",
    author_email="b@palewi.re",
    url="http://www.github.com/palewire/<your-repo-slug>",
    license="MIT",
    packages=("",),  # <--- Your module's directory goes here
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Maintainer": "https://github.com/palewire",
        "Source": "https://github.com/palewire/<your-repo-slug>",
        "Tracker": "https://github.com/palewire/<your-repo-slug>/issues",
    },
)
