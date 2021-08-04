import os
from setuptools import setup


def read(file_name):
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


setup(
    name='<your-pypi-package-name>',
    version='0.0.1',
    description="<your-repo-description>",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Los Angeles Times Data and Graphics Department',
    author_email='datagraphics@caltimes.com',
    url='http://www.github.com/datadesk/<your-repo-slug>',
    license="MIT",
    packages=("<your-python-module-name>",),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
    project_urls={
        'Maintainer': 'https://github.com/datadesk',
        'Source': 'https://github.com/datadesk/<your-repo-slug>',
        'Tracker': 'https://github.com/datadesk/<your-repo-slug>/issues'
    },
)
