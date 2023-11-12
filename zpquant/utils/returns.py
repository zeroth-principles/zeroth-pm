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


"""Weights util file contains ops related to transforming/aggregating weights across cross-sectionally and vertically."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

import pandas as pd
from zpmeta.funcs.func import Func
from pandas import DataFrame, Series, concat, MultiIndex, date_range, IndexSlice
import numpy as np
from datetime import datetime
import logging


class CumulativeReturn_g_AnchorIndex(Func):
    """
    Function class for calculating the cumulative return from daily returns give index.
    """
    @staticmethod
    def _check_consistency(operand=None, params: dict = None):
        if operand is None:
            raise ValueError("operand cannot be None!")
        
        if "index" not in params.keys():
            raise KeyError("Please provide anchor index")
             
    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        """

        Parameters
        ----------
        operand : pd.DataFrame
            The operand here is rebalanced weights.
        period : tuple
            The period is a tuple of (start_datetime, end_datetime).
        params : dict
            The params is a dictionary of parameters.

        Returns
        -------
        pd.DataFrame
            The output is a DataFrame of daily weights.
        """
        anchor_index = params["index"]

        if "period" not in params.keys():
            period = (operand.index[0], operand.index[-1])
        
        ret_temp = operand.truncate(period[0], period[1])
        all_index =  pd.date_range(period[0], period[1], freq="B")
        ret_temp = ret_temp.reindex(all_index).fillna(0.0)
        return_grouped = (1+ret_temp).groupby(anchor_index.searchsorted(ret_temp.index)).cumprod() - 1
        # after groupby names are getting removed from columns
        return_grouped.columns = ret_temp.columns
        return_grouped = return_grouped.fillna(0.0)
        return return_grouped
    