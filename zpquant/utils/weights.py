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
from zpmeta.superclasses.functionclass import FunctionClass
from zputils.dataframe import RandomReturn
from functools import partial
from zpquant.utils.returns import CumulativeReturn_g_index

class DW_g_RW(FunctionClass):
    """
    Function class for calculating the daily weights from rebalanced weights.
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
        return dict(BOD = True, freq = "B", return_param = RandomReturn(params=dict(seed=0, freq="B", distribution = partial(np.random.normal, loc=0.0, scale=1))))

    def __check_consistency(self):
        if "return_param" not in self.params:
            raise KeyError("return_param should be given in params")
        if self.params["return_param"] is None:
            raise ValueError("return_param cannot be None!")
             
    def execute(self, operand: pd.DataFrame =None, period: tuple = None, params: dict = None) -> object:
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
        self.__check_consistency()
        if period is None:
            period = (operand.index[0], operand.index[-1])
        if operand is None:
            raise ValueError("operand cannot be None!")

        if callable(self.params["return_param"]):
            ret_df = self.params["return_param"](entities = operand.columns, period = period)
        else:
            raise NotImplementedError("return calculation is not implemented yet!")
        
        date_range = pd.date_range(period[0], period[1], freq = self.params["freq"])
        #ret_df freq should be same as params freq
        ret_df = ret_df.sort_index().reindex(date_range).fillna(0.0)
        operand = operand.sort_index().truncate(period[0], period[1])
        index = pd.Index(operand.index)
        #if index last value is not equal to end date then add the end date to index
        if index[-1]!=period[1]:
            index = index.append(pd.Index([period[1]]))

        cumulative_ret = CumulativeReturn_g_index(params=dict(index = index))(ret_df)
        dw_eod = operand.fillna(0.0).reindex(date_range).fillna(method = "ffill")* (1+ cumulative_ret)
        dw_eod.loc[operand.index, :] = operand
        
        if self.params["BOD"]:
            dw_bod = dw_eod.shift(1).dropna(how="all", axis=0)
        else:
            dw_bod = dw_eod.copy()

        return dw_bod