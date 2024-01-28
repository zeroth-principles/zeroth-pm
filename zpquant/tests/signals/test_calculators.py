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

"""test_calculators file contains test cases for functions in test_calculators.py"""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

import pandas as pd
import numpy as np
from zpquant.signals.calculators import BinarySignal, RankSignal, ZscoreSignal, NormalizedSignal

def test_binary_signal():
    signal = BinarySignal()
    operand = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
    result = signal(operand)
    assert result.equals(pd.DataFrame({'A': [1, 1, 1, 1, 1]}))

def test_rank_signal():
    params = dict(rank_param = dict(axis=1), centered = True)
    signal = RankSignal(params = params)
    operand = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
    result = signal(operand)
    assert result.equals(pd.DataFrame({'A': [-1.0, -1.0, 0.0, 1.0, 1.0], 'B': [1.0, 1.0, 0.0, -1.0, -1.0]}))
    assert RankSignal.check_consistency(params = signal.params) == True
    
def test_zscore_signal():
    params = dict(axis=1)
    signal = ZscoreSignal(params = params)
    operand = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
    result = signal(operand)
    assert result.round(6).equals(pd.DataFrame({'A': [-0.707107, -0.707107, np.nan, 0.707107, 0.707107], 'B': [0.707107, 0.707107, np.nan, -0.707107, -0.707107]}))

def test_normalized_signal():
    params = dict(axis=1)
    signal = NormalizedSignal(params = params)
    operand = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
    result = signal(operand)
    assert result.round(6).equals(pd.DataFrame({'A': [-0.707107, -0.707107, np.nan, 0.707107, 0.707107], 'B': [0.707107, 0.707107, np.nan, -0.707107, -0.707107]}))
