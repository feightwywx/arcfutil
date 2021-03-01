import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="arcfutil",
    version="0.3.1",
    author=".direwolf",
    author_email="kururinmiracle@outlook.com",
    description="A Python module designed for processing Arcaea related files(.aff chart, songlist, etc.)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/feightwywx/arcfutil",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    entry_points={"console_scripts": [
        "arcfutil = arcfutil.cli:main",
        "songlist = arcfutil.songlist:main",
        "sortassets = arcfutil.sortassets:main"
        ]
    }
)
