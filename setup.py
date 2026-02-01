"""Setup configuration for JDevtools."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="jdevtools",
    version="0.1.0",
    description="Curated Dev tools for creating native apps in Core Java and Java",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="JDevtools",
    python_requires=">=3.7",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jcompile-dispatch=jdevtools.jcompile_dispatch:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
