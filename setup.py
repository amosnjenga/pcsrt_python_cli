import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="pcsrt-cli-python-tool",
    version="1.0.0",
    author="Anastasia Anastasia",
    author_email="nastyaenn@gmail.com",
    description=("A tool for modeling solar radiation & insolation "
                 "on point cloud data built in Python."),
    url="https://github.com/amosnjenga/pcsrt_python_cli",
    project_urls={
        "Bug Tracker": " ",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["laspy==2.4.1","plyfile==0.9","pvlib==0.9.5","numpy==1.24.3",
                      "python-dateutil==2.8.2","pytz==2023.3","scikit-learn==1.2.2","scipy==1.10.1"],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pcsrt = pcsrt.cli_main:main",
        ]
    }
)