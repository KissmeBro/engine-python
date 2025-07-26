from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="engine-python",
    version="1.1.0",
    description="An intelligent, asynchronous search engine library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="stone",
    author_email="kissme.cloud@example.com",
    url="https://github.com/kissmeBro/engine-python",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "aiohttp",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)