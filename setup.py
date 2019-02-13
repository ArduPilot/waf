import setuptools
import waflib.Context

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="waf",
    version=waflib.Context.WAFVERSION,
    author="Thomas Nagy",
    author_email="author@example.com",
    description="Build Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ita1024/waf",
    packages=['waflib', 'waflib/Tools', 'waflib/extras'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
