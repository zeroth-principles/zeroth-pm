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

"""test_weights file contains test cases for weights util file in zpquant"""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']


import pytest
import pandas as pd
import numpy as np
from functools import partial
from zpquant.utils.returns import CumulativeReturn_g_AnchorIndex
from zputils.dataframes.simulated import SimulatedDataFrame
from pandas import testing as tm


def test_cumulative_return_with_valid_input():
    rr = SimulatedDataFrame(params={'seed': 0, 'freq': 'B', 'distribution': partial(np.random.normal, loc=0.0, scale=0.05)})
    operand = rr(entities=['A', 'B'], period=('2022-01-01', '2022-01-30'))

    func = CumulativeReturn_g_AnchorIndex(params = dict(index = pd.date_range('2022-01-01', '2022-01-30', freq='w-MON')))
    result = func(operand= (operand))
    # Assert based on expected output
    assert isinstance(result, pd.DataFrame)
    assert len(result)==20
    # last_data = pd.Series({'A': -0.004047, 'B': -0.009475}, name = pd.to_datetime('2022-01-28'))
    # assert result.iloc[-1].val==last_data

