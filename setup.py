# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Zeroth-Principles
#
# This file is part of Zeroth-Quant.
#
#  Zeroth-Quant is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Zeroth-Quant is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Zeroth-Quant. If not, see <http://www.gnu.org/licenses/>.f

from setuptools import setup, find_packages
import os

def get_local_path(name):
    """
    Dynamically determine the path to Repo.
    """
    local_name = name
    local_path = os.getcwd().split(os.sep)
    local_path = os.sep.join(local_path[:-1])
    local_path = os.path.join(local_path, local_name)
    return local_path

# dynamically determine the path to Repo1
local_name1 = "zeroth-meta"
local_path1 = get_local_path(local_name1)
# dynamically determine the path to Repo2
local_name2 = "zeroth-utils"
local_path2 = get_local_path(local_name2)

setup(
    name="zeroth-quant",
    version="1.0.0",
    description="Quant Repo",
    author = "Zeroth-Principles",
    author_email = "engineering@zeroth-principles.com",
    license="GPLv3",
    url="https://zeroth-principles.com",
    # python_requires=">=3.5.0",
    # packages = find_packages(where="zeroth-meta"),
    packages = find_packages(),
    # package_dir={'': "zeroth-meta"},
    install_requires=[],
    extras_require={},
)