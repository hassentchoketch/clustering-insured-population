import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
    
__version__ = "0.0.1"

repository_name = "clustering-insured-population"
author_user_name = "hassentchoketch"
author_email = "hassentchoketch@gmail.com"
SRC_REPO = "insuredSegmenter"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=author_user_name,
    author_email=author_email,
    description="A small package for clustering insured population app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"http://github.com/{author_user_name}/{repository_name}",
    project_urls={
        "Bug Tracker": f"http://github.com/{author_user_name}/{repository_name}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)