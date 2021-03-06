import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trove",
    version="0.1",
    author="Zach Hafen",
    author_email="zachary.h.hafen@gmail.com",
    description="Analysis pipeline construction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhafen/trove",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=[ 'trove/bin/trove' ],
    # install_requires=[
    #     'bibtexparser>=1.2.0',
    #     'tqdm>=4.46.0',
    #     'palettable>=3.3.0',
    #     'numba>=0.51.2',
    #     'plotly>=4.11.0',
    #     'nltk>=3.5',
    #     'matplotlib>=3.2.2',
    #     'ads>=0.12.3',
    #     'numpy>=1.19.1',
    #     'pytest>=6.0.1',
    #     'scipy>=1.5.0',
    #     'simple-augment>=1.0',
    #     'mock>=4.0.2',
    #     'pandas>=1.1.4',
    #     'rebound>=3.12.3',
    #     'verdict>=1.1.4',
    # ],
)
