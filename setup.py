import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="svis",
    version="0.0.1",
    author="Sophia Sanborn",
    author_email="sophia.sanborn@gmail.com",
    description="A collection of visualization tools commonly used in my research.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sophiaas/visualizations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
