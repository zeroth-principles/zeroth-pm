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


"""Signal class take the feature and transform it based on the input."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

import pandas as pd
import numpy as np
from zpmeta.sources.panelsource import PanelSource
from zpmeta.singletons.singletons import MultitonMeta
from zpquant.signals.mapping import feature_mapping, signal_calculation_mapping
from zpquant.signals.calculators import *


class Signal(PanelSource, metaclass=MultitonMeta):
    '''
    Subclasses PanelCachedSource to transform the feature values based on the input.

    Attributes:
            feature_name: str
                Name of the feature. Example: "EQPriceMomentum"

            feature_params: dict
                Parameters to run the feature. Example: {"lookback_period": 12, axis = 0}

            transform_pipeline: dict
                Parameters to transform the feature value. Example: {"zscoreXS": None}

    Methods:
            check_consistency: method
                Check the consistency of the input parameters

            _execute: method
                Execute the signal calculation

    Examples:
            # to calculate cross-sectional zscore of 12 day price momentum
            >>> from zpquant.signals.signal import Signal
            >>> signal = Signal(params = {"feature_name": "EQPriceMomentum", "feature_params": {"lookback_period": 12, axis = 0}, "transform_pipeline": {"zscoreXS": None}})
            >>> signal(entities=entities, period=period)
     
    '''
    def __init__(self, params: dict = None):
        super(Signal, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)

    @staticmethod
    def check_consistency(params):
        if "feature_name" not in params.keys():
            raise KeyError("Please provide the name of the feature")
        
        if "feature_params" not in params.keys():
            raise KeyError("Please provide the config to run the feature")
        
        if "transform_pipeline" not in params.keys():
            raise KeyError("Please provide the transform params. If None then feature value will be taken as it is.")
        
        if not isinstance(params["transform_pipeline"], dict):
            raise ValueError("transform_pipeline should be a dict")
        return True
             
    def _execute(self, entities=None, period=None):
        signal_value = feature_mapping[self.params.get("feature_name")](self.params.get("feature_params"))(entities=entities, period=period)

        # apply weighting methodology
        for transformation in self.params["transform_pipeline"].keys():
            try:
                signal_value = signal_calculation_mapping[transformation](params = self.params["transform_pipeline"].get(transformation))(signal_value)
            except KeyError:
                raise KeyError("Please provide the correct transformation name")

        return signal_value