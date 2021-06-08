
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lambda-proxy-helpers",
    version="0.0.4",
    author="Peter Deppe",
    author_email="",
    description="Package of common utility/helper functions for Lambda Poxy development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/depster26/lambda-proxy-helpers.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
