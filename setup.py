from setuptools import setup, find_packages

setup(
    name="pyfilecache",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="HellOwhatAs",
    author_email="xjq701229@outlook.com",
    description="cache results of slow function to disk",
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