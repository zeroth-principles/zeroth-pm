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


"""Weights util file contains ops related to transforming/aggregating weights across cross-sectionally and vertically."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

import pandas as pd
import numpy as np
from zpmeta.funcs.func import Func
from zputils.dataframes.simulated import SimulatedDataFrame
from functools import partial
from zpquant.utils.returns import CumulativeReturn_g_AnchorIndex


class PPW_g_RW(Func):
    """
    # TODO: change to ppw_g_rw

    Function class for calculating the daily weights given rebalanced weights.
    """

    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        """
        Standard parameters for the function class.
        return: dict
            BOD: bool
                Whether the output weight is beginning of day or end of day.
            freq: str
                The frequency of the output weights.

            return_param: callable or params dict
                If callable then directly called otherwise currently not implemented
        """
        return dict(BOD = True, freq = "B")
    @staticmethod
    def check_consistency(operand=None, params: dict = None):
        if operand is None:
            raise ValueError("operand cannot be None!")
    
            
    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        """

        Parameters
        ----------
        operand : pd.DataFrame
            The operand here contains weight
        period : tuple
            The period is a tuple of (start_datetime, end_datetime).
        params : dict
            The params is a dictionary of parameters.

        Returns
        -------
        pd.DataFrame
            The output is a DataFrame of daily weights.
        """
        # fetch the return dataframe
        # TODO: Add Return class here, currently just passing None
        params["return"] = None
        dw = PPW_g_RW_g_R(params)(operand)

        return dw
    
class PPW_g_RW_g_R(Func):
    """
    Function class for calculating the daily weights given rebalanced weights and returns dataframe.
    """

    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        """
        Standard parameters for the function class.
        return: dict
            BOD: bool
                Whether the output weight is beginning of day or end of day.
            freq: str
                The frequency of the output weights.

            return_param: callable or params dict
                If callable then directly called otherwise currently not implemented
        """
        return dict(BOD = True, freq = "B", return_param = SimulatedDataFrame(params=dict(seed=0, freq="B", distribution = partial(np.random.normal, loc=0.0, scale=0.05))))

    @staticmethod
    def check_consistency(operand: pd.DataFrame =None, params: dict = None):
        if operand is None:
            raise ValueError("operand cannot be None!")
        
        
        if "return" not in params.keys():
            raise KeyError("Please provide return dataframe")

        elif params["return"] is None:
            if "return_param" not in params.keys():
                raise KeyError("If return data is none then return param should not be none")
            
            if not callable(params["return_param"]):
                raise NotImplementedError("Pass the callable return param")
            
    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        """

        Parameters
        ----------
        operand : tuple
            The operand here contains weight and return as tuple
        period : tuple
            The period is a tuple of (start_datetime, end_datetime).
        params : dict
            The params is a dictionary of parameters.

        Returns
        -------
        pd.DataFrame
            The output is a DataFrame of daily weights.
        """
        rw = operand.copy()
        ret_df = params["return"]
        if "period" not in params.keys():
            period = (rw.index[0], rw.index[-1])
        
        if ret_df is None:
            ret_df = params["return_param"](entities = list(rw.columns), period = period)
        
        date_range = pd.date_range(period[0], period[1], freq = params["freq"])
        #ret_df freq should be same as params freq
        ret_df = ret_df.sort_index().reindex(date_range).fillna(0.0)
        rw = rw.sort_index().truncate(period[0], period[1])
        index = pd.Index(rw.index)
        #if index last value is not equal to end date then add the end date to index
        if index[-1]!=period[1]:
            index = index.append(pd.Index([period[1]]))

        cumulative_ret = CumulativeReturn_g_AnchorIndex(params = dict(index = index))(ret_df)
        dw_eod = rw.fillna(0.0).reindex(date_range).fillna(method = "ffill")* (1+ cumulative_ret)
        dw_eod.loc[rw.index, :] = rw
        
        if params["BOD"]:
            dw_bod = dw_eod.shift(1).dropna(how="all", axis=0)
        else:
            dw_bod = dw_eod.copy()

        return dw_bod