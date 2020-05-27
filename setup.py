from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ACI-L3OUT-Modular",
    version="1.1.0",
    author="Graber, Andreas",
    author_email="graber@netcloud",
    packages=['L3Out'],
    url="https://github.com/netcloudag/AciL3outModular.git",
    license="MIT - See LICENSE.md file",
    description="Python Modul for Generation L3Outs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7.X",
        "Topic :: System :: Networking",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Utilities",
        "License :: Other/Proprietary License",
    ],
    keywords="ACI SDN L3OUT",
)
