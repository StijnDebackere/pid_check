import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pid_check",
    version="0.0.1",
    author="Stijn Debackere",
    author_email="debackere@strw.leidenuniv.nl",
    description="Notify user when processes finish.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['pid_check'],
    entry_points={
        "console_scripts": [
            "watchpids = pid_check.daemon:main",
            "addpid = pid_check.add_pid:main",
        ],
    },
    install_requires=[
        "psutil",
        "python-daemon",
        "toml",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
