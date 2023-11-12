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
#

"""Superclasses for frequently used design patterns."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']
__all__ = ["BinarySignal", "RankSignal", "ZscoreSignal", "NormalizedSignal"]

import pandas as pd
from zpmeta.funcs.func import Func
import numpy as np
from scipy.stats import zscore
from zpmath.scaler import ZscoreScaler, NormalScaler

class BinarySignal(Func):
    """
    Function will return binary signal i.e +-1
    """
    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        return np.sign(operand)


class RankSignal(Func):
    """
    Function class for calculating the cross-sectional rank given dataframe.
    """
    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        """
        Standard parameters for the function class.
        return: dict
            For following params (axis, method, numeric_only, na_option, ascending, pct)
            please look at pandas documentation of rank method.

            centered: bool
                If true then rank will be centered around zero

        """
        return dict(axis=1, method='average', numeric_only=False, na_option='keep', ascending=True, pct=False, centered = True)
    
    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        if isinstance(operand, pd.Series):
            operand = operand.to_frame("temp_series_name")
            params["axis"] = 0

        rankDf = operand.rank(axis= params["axis"], method= params["method"], numeric_only= params["numeric_only"], 
                              na_option=params["na_option"], ascending= params["ascending"], pct= params["pct"])

        if params["centered"]:
            midRank = rankDf.mean(axis= params["axis"], skipna=True)
            rankDf = rankDf.apply(lambda x: midRank - x, axis= 0 if params["axis"]==1 else 0)
            # make long short sum to +1 and -1
            rankDf[rankDf>0] = rankDf[rankDf>0].div(np.abs(rankDf[rankDf>0]).sum(axis= params["axis"]), axis = 0 if params["axis"]==1 else 0)
            rankDf[rankDf<0] = rankDf[rankDf<0].div(np.abs(rankDf[rankDf<0]).sum(axis= params["axis"]), axis = 0 if params["axis"]==1 else 0)

        if isinstance(operand, pd.Series):
            rankDf = rankDf["temp_series_name"]

        return rankDf
    
class ZscoreSignal(Func):
    """Function class for calculating the zscore given dataframe."""

    def std_params(self, name: str = None) -> dict:
        """
        Standard parameters for the function class.
        return: dict
            axis : {0 or 'index', 1 or 'columns'}, default 1

            winsorize_method : str
                "zp": zp winsorization method, uses recursize methodology
                "scipy": scipy winsorization method, uses scipy.stats.mstats.winsorize

            winsorize_params : dict
                Below params are for zp method
                    max_score : float
                    Threshold for winsorizing the data, here score represents number of standard deviation away.
                
                    eps : float
                        eps is the margin of error that is accepted around max score to get the solution avoid recurssion error.

                Below params are for scipy method
                    Look at the documentation of scipy.stats.mstats.winsorize


        """
        return dict(axis=1, winsorize_method = "zp", winsorize_params = dict(max_score = 2.8, eps = 0.3))
    
    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        zscore_df = ZscoreScaler(params=params)(operand)
        return zscore_df
    
class NormalizedSignal(Func):
    """Function class for calculating the normalized signal given dataframe."""

    def std_params(self, name: str = None) -> dict:
        """
        Standard parameters for the function class.
        return: dict
            axis : {0 or 'index', 1 or 'columns'}, default 1

        """
        return dict(axis=1)
    
    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        normal_df = NormalScaler(params=params)(operand)
        return normal_df