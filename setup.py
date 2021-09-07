from setuptools import setup, find_packages

import remote_minerl_env

with open("Readme.md") as f:
    long_description = f.read()

setup(
    name="remote_minerl_env",
    version=remote_minerl_env.__version__,
    author="infinityofspace",
    url="https://github.com/infinityofspace/remote_minerl_env",
    description="Remote environment for minerl competition environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "minerl>=0.3.6",
        "pyngrok>=5.1.0"
    ],
    entry_points={
        "console_scripts": [
            "remote-minerl-env=remote_minerl_env.cli:main",
        ]
    }
)
