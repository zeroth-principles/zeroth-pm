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


"""File calculates the momentum feature given return series."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']
__all__ = ["PriceMomentum_g_Returns", "PriceMomentum"]

from functools import partial
from zpmeta.funcs.func import Func
import numpy as np
import pandas as pd
from zpmeta.sources.panelsource import PanelSource
from zpmeta.singletons.singletons import MultitonMeta
from zputils.dataframes.simulated import SimulatedDataFrame
from zputils.dict.update import deep_update
from pandas.tseries.offsets import BDay
from zpquant.features.base.feature import EQFactor, FUFactor

class PriceMomentum_g_Returns(Func):
    """
    Function class for calculating the price momentum given returns.
    """
    def _std_params(self, name: str = None) -> dict:
        """
        Standard parameters for the function class.
        return: dict
            lookback_period : int
                Number of days to look back for calculating the momentum
            
            axis : {0 or 'index', 1 or 'columns'}, default 1
        """
        return dict(lookback_period=252, axis=0)
    
    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        momentum = operand.rolling(window=params["lookback_period"], axis = params["axis"], 
                                   min_periods=int(0.5 * params["lookback_period"])).apply(
                                       lambda x: np.prod(1+x)-1, raw=True).dropna(how="all")
        return momentum


class EQPriceMomentum(EQFactor):
    '''Subclasses Equity factor base class to calculate momentum feature values.'''
    def __init__(self, params: dict = None):
        """
        params: dict
            lookback_period : int
                Number of days to look back for calculating the momentum
            
            axis : {0 or 'index', 1 or 'columns'}, default 1

            asset_class: str
                Asset class for which the feature value is calculated
        """
        super(EQPriceMomentum, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)
             
    def _execute(self, entities=None, period=None):
        data_period = (period[0] - BDay(self.params["lookback_period"]), period[1])
        if self.params.get("simulation", False):
            return_df = SimulatedDataFrame(params=dict(seed=0, freq="B", distribution = partial(np.random.normal, loc=0.0, scale=0.05)))(entities=entities, period=data_period)
        else:
            # get eq returns
            raise NotImplementedError("Equity returns not implemented yet")
        momentum_df = PriceMomentum_g_Returns(params= self.params)(return_df)
        
        return momentum_df

class FUPriceMomentum(FUFactor):
    '''Subclasses Future factor to calculate momentum feature values.'''
    def __init__(self, params: dict = None):
        """
        params: dict
            lookback_period : int
                Number of days to look back for calculating the momentum
            
            axis : {0 or 'index', 1 or 'columns'}, default 1

            asset_class: str
                Asset class for which the feature value is calculated
        """
        super(FUPriceMomentum, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)
             
    def _execute(self, entities=None, period=None):
        data_period = (period[0] - BDay(self.params["lookback_period"]), period[1])
        if self.params.get("simulation", False):
            return_df = SimulatedDataFrame(params=dict(seed=0, freq="B", distribution = partial(np.random.normal, loc=0.0, scale=0.05)))(entities=entities, period=data_period)
        else:
            # get eq returns
            raise NotImplementedError("Future returns not implemented yet")
        momentum_df = PriceMomentum_g_Returns(params= self.params)(return_df)
        
        return momentum_df
