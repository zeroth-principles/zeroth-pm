# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Zeroth-Principles
#
# This file is part of Zeroth-Meta.
#
#  Zeroth-Meta is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
# 
#  Zeroth-Meta is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Zeroth-Meta. If not, see <http://www.gnu.org/licenses/>.

"""test_feature file contains test cases for EQFactor and FUFactor class in feature.py"""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

import pytest
from zpquant.features.base.feature import EQFactor, FUFactor

@pytest.fixture
def eq_factor():
    return EQFactor(params=None)

@pytest.fixture
def fu_factor():
    return FUFactor(params=None)

def test_eq_factor_init(eq_factor):
    assert isinstance(eq_factor, EQFactor)

def test_fu_factor_init(fu_factor):
    assert isinstance(fu_factor, FUFactor)


