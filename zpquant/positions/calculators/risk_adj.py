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


"""This file has functions to convert the signal into dollar neutral, beta neutral positions."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']
__all__ = ["DollarNeutral", "BetaNeutral"]

class GrinoldWeighting(Func):
    """
    Function class to convert signal into positions.This is based on the paper Signal Weighting by Richard Grinold.
    https://www.pm-research.com/content/iijpormgmt/36/4/24

    Attributes:
        axis: int
            Axis to calculate the dollar neutral position
    
    Methods:
        _execute: method
            Execute the position calculation
    
    Examples:
    
    """
    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        return dict(axis = 1)

    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        position = operand.copy()
        
        return position    

# def calculate_grinold_weighting(scores: pd.Series, dataset:DataSet):
#     non_nan_scores = scores.dropna()
#     vcv_inv = Position.calculate_stock_vcv_inverse(non_nan_scores.index, non_nan_scores.name, dataset)
#     non_nan_scores = non_nan_scores.reindex(vcv_inv.index)
#     den = np.sqrt(non_nan_scores.values.T @ vcv_inv @ non_nan_scores.values)
#     num = vcv_inv @ non_nan_scores.values
#     wt = pd.Series(data = num/den, index = non_nan_scores.index)
#     wt = wt.reindex(scores.index)
#     wt.name = scores.name
#     return wt