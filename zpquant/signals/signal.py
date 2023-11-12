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
from zpmeta.funcs.func import Func
from zpmeta.sources.panelsource import PanelSource
from zpmeta.singletons.singletons import MultitonMeta
from zpquant.signals.mapping import featureMapping
from zpquant.signals.calculators import *


class Signal(PanelSource, metaclass=MultitonMeta):
    '''Subclasses PanelCachedSource to transform the feature values based on the input.'''
    def __init__(self, params: dict = None):
        super(Signal, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)

    @staticmethod
    def _check_consistency(params):
        if "featureName" not in params.keys():
            raise KeyError("Please provide the name of the feature")
        
        if "featureParams" not in params.keys():
            raise KeyError("Please provide the config to run the feature")
        
        if "transform" not in params.keys():
            raise KeyError("Please provide the transform params. If None then feature value will be taken as it is.")
             
    def _execute(self, entities=None, period=None):
        featureValue = featureMapping[self.params["featureName"]](self.params["featureParams"])(entities=entities, period=period)

        if self.params["transform"] is None:
            return featureValue
        elif self.params["transform"] == "zscoreXS":
            # do cross-sectional zscore
            signalValue = ZscoreSignal(params = self.params)(operand=featureValue, params=dict(axis=1))
            
        elif self.params["transform"] == "zscoreTS":
            # do time series zscore
            signalValue = ZscoreSignal(params = self.params)(operand=featureValue, params=dict(axis=0))
        elif self.params["transform"] == "rankXS":
            # do cross-sectional ranking
            signalValue = RankSignal(params = self.params)(operand=featureValue, params=dict(axis=1))
        elif self.params["transform"] == "rankTS":
            # do time series ranking
            signalValue = RankSignal(params = self.params)(operand=featureValue, params=dict(axis=0))
        elif self.params["transform"] == "equal":
            # do equal weighting
            raise NotImplementedError
        elif self.params["transform"] == "value":
            # do equal weighting
            signalValue = featureValue.copy()
        else:
            # do equal weighting
            raise NotImplementedError
        

        return signalValue