import setuptools
from setuptools import find_namespace_packages

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="arcfutil",
    version="0.11.0",
    author=".direwolf",
    author_email="kururinmiracle@outlook.com",
    description="A Python module designed for processing Arcaea related files(.aff chart, songlist, etc.)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/feightwywx/arcfutil",
    packages=find_namespace_packages('src', include=['arcfutil.*']),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    entry_points={"console_scripts": [
        "arcfutil = arcfutil.cli:main",
        "songlist = arcfutil.cli.songlist:main",
        "sortassets = arcfutil.cli.sortassets:main",
        "arcadeclean = arcfutil.cli.arcade_clean:main"
        ]
    },
    zip_safe=False,
)
