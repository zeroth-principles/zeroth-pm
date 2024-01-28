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

"""test_signal file contains test cases for signal class in signal.py"""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']
import pytest
from zpquant.signals.signal import Signal
from datetime import datetime

class TestSignal:
    def test_check_consistency(self):
        params = {
            "feature_name": "EQPriceMomentum",
            "feature_params": {"lookback_period": 12, "axis": 0},
            "transform_pipeline": {"zscoreXS": None}
        }
        signal = Signal(params=params)
        assert signal.check_consistency(params) == True

    def test_execute(self):
        entities = dict(A = ['AAPL', 'GOOG'])
        period = (datetime(2022, 1, 1), datetime(2022, 1, 30))
        params = {
            "feature_name": "EQPriceMomentum",
            "feature_params": {"lookback_period": 12, "axis": 0, "simulation": True},
            "transform_pipeline": {"zscoreXS": None, "rankTS": None}
        }
        signal = Signal(params=params)
        signal_value = signal(entities=entities, period=period)
        assert len(signal_value) == 30
        
