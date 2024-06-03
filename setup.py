from setuptools import setup, find_packages

setup(
    name="pyfilecache",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        'filelock'
    ],
    author="HellOwhatAs",
    author_email="xjq701229@outlook.com",
    description="cache the results of slow-running functions to disk, with multi-process safety",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/HellOwhatAs/pyfilecache",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)