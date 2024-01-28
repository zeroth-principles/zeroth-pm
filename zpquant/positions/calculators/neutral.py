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

import pandas as pd
import numpy as np

from zpmeta.funcs.func import Func


class DollarNeutral(Func):
    """
    Function class to convert signal into dollar neutral positions.

    Attributes:
        axis: int
            Axis to calculate the dollar neutral position
    
    Methods:
        _execute: method
            Execute the position calculation
    
    Examples:
        # to calculate dollar neutral position
        >>> from zpquant.positions.calculators.neutral import DollarNeutral
        >>> position = DollarNeutral(params = {"axis": 1})(signal_value, params = None)
    
    """
    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        return dict(axis = 1)

    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        position = operand.copy()
        position[position>0] = position[position>0].div(np.abs(position[position>0]).sum(axis= 
                                        params["axis"]), axis = 0 if params["axis"]==1 else 0)
        position[position<0] = position[position<0].div(np.abs(position[position<0]).sum(axis= 
                                        params["axis"]), axis = 0 if params["axis"]==1 else 0)

        return position


class BetaNeutral(Func):
    """
    Function class to convert signal into beta neutral positions.

    Attributes:
        axis: int
            Axis to calculate the beta neutral position
    
    Methods:
        _execute: method
            Execute the position calculation
    
    Examples:
        # to calculate beta neutral position
        >>> from zpquant.positions.calculators.neutral import BetaNeutral
        >>> position = BetaNeutral(params = {"axis": 1})(signal_value, params = None)
    
    """
    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        return dict(axis = 1)

    def _execute(self, operand: pd.DataFrame =None, params: dict = None) -> object:
        position = operand.copy()
        # get beta values for each entity
    

        raise NotImplementedError("BetaNeutral not implemented yet")

        return position