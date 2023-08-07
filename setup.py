from setuptools import setup, find_packages
import os

# dynamically determine the path to Repo2
local_name = "zeroth-meta"
local_path = os.getcwd().split(os.sep)
local_path = os.sep.join(local_path[:-1])
local_path = os.path.join(local_path, local_name)

setup(
    name="zeroth-quant",
    version="1.0.0",
    description="Quant Repo",
    # python_requires=">=3.5.0",
    packages = find_packages(where = "zpquant"),
    package_dir={'': "zpquant"},
    install_requires=[
        f"{local_name} @ file://localhost/{local_path}#egg={local_name}"
    ]
)