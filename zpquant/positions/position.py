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
from zpquant.positions.mapping import weightMapping

class Position(PanelSource, metaclass=MultitonMeta):
    '''Subclasses PanelCachedSource to transform the feature values based on the input.'''
    def __init__(self, params: dict = None):
        super(Position, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)

    @staticmethod
    def _check_consistency(params):
        if "signalParams" not in params.keys():
            raise KeyError("Please provide the config to run the signal")
        
        if "weightingPipeline" not in params.keys():
            raise KeyError("Please provide the weighting method for calculating positions")
            
        if not isinstance(params["weightingPipeline"], dict):
            raise ValueError("weightingPipeline should be a list of weighting methods dictionaries")
                
    def _execute(self, entities=None, period=None):
        # get signal value
        signal_value = Signal(params = self.params["signalParams"])(entities=entities, period=period)

        position_value = signal_value.copy()
        # apply weighting methodology
        for weighting_method in self.params["weightingPipeline"].keys():
            position_value = weightMapping[weighting_method](params = self.params["weightingPipeline"][weighting_method])(position_value)

        return position_value
    