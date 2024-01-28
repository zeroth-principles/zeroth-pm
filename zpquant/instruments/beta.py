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


"""This file either fetch the predicted beta from database or calculate the beta from the returns."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']
__all__ = ["PBeta", "EQPBeta", "FUPBeta"]

from zpmeta.funcs.func import Func
import numpy as np
import pandas as pd
from zpmeta.sources.panelsource import PanelSource
from zpmeta.singletons.singletons import MultitonMeta

class PBeta(PanelSource, metaclass=MultitonMeta):
    """
    """
    def __init__(self, params: dict = None):
        super(PBeta, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)

    @staticmethod
    def check_consistency(params):
        pass

    def _execute(self, entities=None, period=None):
        raise NotImplementedError("PBeta is not implemented")