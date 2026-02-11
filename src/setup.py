"""
SecurePass Toolkit - Password Security Analysis Suite
Entry-level cybersecurity project for portfolio building
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="securepass",
    version="1.0.0",
    author="Richard Blea",
    author_email="rblea97@gmail.com",
    description="A professional CLI password security analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rblea97/password-security-toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/Rblea97/password-security-toolkit/issues",
        "Documentation": "https://github.com/Rblea97/password-security-toolkit#readme",
        "Source Code": "https://github.com/Rblea97/password-security-toolkit",
    },
    packages=find_packages(),
    keywords=[
        "password",
        "security",
        "cli",
        "cybersecurity",
        "entropy",
        "breach-detection",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "securepass=securepass.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "securepass": ["../data/*.txt"],
    },
)
