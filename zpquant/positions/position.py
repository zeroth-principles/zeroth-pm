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


"""Position class take the signal and output the weights based on the input."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

import pandas as pd
import numpy as np
from zpmeta.funcs.func import Func
from zpmeta.sources.panelsource import PanelSource
from zpmeta.singletons.singletons import MultitonMeta
from zpquant.positions.calculators import *
from zpquant.signals.signal import Signal
from zpquant.positions.mapping import weight_mapping

class Position(PanelSource, metaclass=MultitonMeta):
    '''
    Subclasses PanelCachedSource to transform the signal values to positions.
    
    Attributes:
            signal_params: dict
                Parameters to run the signal. 
                Example: {{"feature_name": "EQPriceMomentum", "feature_params": {"lookback_period": 12, axis = 0}, 
                         "transform_pipeline": {"zscoreXS": None}}}
    
            weighting_pipeline: dict
                Parameters to transform the signal value to position. Example: {"dollar_neutral": None}
    
    '''
    def __init__(self, params: dict = None):
        super(Position, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)

    @staticmethod
    def check_consistency(params):
        if "signal_params" not in params.keys():
            raise KeyError("Please provide the config to run the signal")
        
        if "weighting_pipeline" not in params.keys():
            raise KeyError("Please provide the weighting method for calculating positions")
            
        if not isinstance(params["weighting_pipeline"], dict):
            raise ValueError("weighting_pipeline should be a dict")
                
    def _execute(self, entities=None, period=None):
        # get signal value
        signal_value = Signal(params = self.params["signal_params"])(entities=entities, period=period)

        position_value = signal_value.copy()
        # apply weighting methodology
        for weighting_method in self.params["weighting_pipeline"].keys():
            position_value = weight_mapping[weighting_method](params = self.params["weighting_pipeline"][weighting_method])(position_value)

        return position_value
    