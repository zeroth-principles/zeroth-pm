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
#  Zeroth-Quant. If not, see <http://www.gnu.org/licenses/>.

"""file contains ops related to calculatig financial time-series momentum."""

__copyright__ = '2023 Zeroth Principles'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'


from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas
import numpy
from pandas import date_range
from copy import deepcopy
import logging

from zpmeta.superclasses.panelcachedsource import PanelCachedSource
from zpmeta.superclasses.functionclass import FunctionClass
from zputils.dataframes.timeops import shift_g_df


class momentum_g_prices(FunctionClass):
    @classmethod
    def _std_params(cls, name=None) -> dict:
        if name is None:
            params = dict(lookback_period=None, skip_period = None)
        return params
    
    @classmethod
    def _execute(cls, operand=None, period: tuple = None, params: dict = None) -> object:
        logging.debug('params: {}'.format(params))

        lagged1 = shift_g_df(params=dict(periods=params['lookback_period'], align=True))(operand)
        lagged2 = shift_g_df(params=dict(periods=params['skip_period'], align=True))(operand)
        
        mom = (1.0 - lagged2.div(lagged1)).dropna(how='all')
        
        return mom
    

class momentum_g_returns(FunctionClass):
    @classmethod
    def _std_params(cls, name=None) -> dict:
        if name is None:
            params = dict(lookback_period=None, skip_period = None)
        return params
    
    @classmethod
    def _execute(cls, operand=None, period: tuple = None, params: dict = None) -> object:
        logging.debug('params: {}'.format(params))
        
        lagged1 = shift_g_df(params=dict(periods=params['lookback_period']))(operand)
        lagged2 = shift_g_df(params=dict(periods=params['skip_period']))(operand)
        
        mom = (1.0 - lagged2.div(lagged1)).dropna(how='all')
        
        return mom
    
    