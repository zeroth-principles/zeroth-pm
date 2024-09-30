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

"""This module sets the config for any equity factor """

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

__author__ = "deepak"
__email__ = "deepaksinghcws@gmail.com"
__all__ = ['EQFactor', 'FUFactor']

import pandas as pd
import numpy as np
import logging
from zpmeta.sources.panelsource import PanelSource
from zpmeta.singletons.singletons import MultitonMeta


class EQFactor(PanelSource, metaclass=MultitonMeta):
	"""
	Base class for equity factor

	"""
	def __init__(self, params: dict = None):
		"""
		Standard parameters for the function class.
		params: dict
			ffill: bool
				Forward fill the data
			lag : int
				Number of days to lag the data
		"""
		super(EQFactor, self).__init__(params)
		self.appendable = dict(xs=True, ts=True)

	def _wrapped_execute(self, call_type=None, entities=None, period=None):
		"""
		Parameters:
		----------

		period: datetime tuple
			Tuple containing start and end date

		universe: list
			List containing universe

		Returns:
			Factor object

		"""
		period_log = period if period is not None else (None, None)
		logging.info("EXEC %s: [%s] %s - %s" %(call_type, str(entities), *period_log))
		results = self._execute(entities=entities, period=period)
		results = results.reindex(pd.date_range(period[0], period[1], freq="D"))

		if self.params.get("ffill", False):
			results = results.fillna(method="ffill")

		if self.params.get("lag", None) is not None:
			results = results.shift(self.params["lag"]).dropna(how="all")
		return results
	


class FUFactor(PanelSource, metaclass=MultitonMeta):
	"""
	Base class for equity factor

	"""
	def __init__(self, params: dict = None):
		"""
		Standard parameters for the function class.
		params: dict
			ffill: bool
				Forward fill the data
			lag : int
				Number of days to lag the data
		"""
		super(FUFactor, self).__init__(params)
		self.appendable = dict(xs=True, ts=True)

	def _wrapped_execute(self, call_type=None, entities=None, period=None):
		"""
		Parameters:
		----------

		period: datetime tuple
			Tuple containing start and end date

		universe: list
			List containing universe

		Returns:
			Factor object

		"""
		period_log = period if period is not None else (None, None)
		logging.info("EXEC %s: [%s] %s - %s" %(call_type, str(entities), *period_log))
		results = self._execute(entities=entities, period=period)
		results = results.reindex(pd.date_range(period[0], period[1], freq="D"))

		if self.params.get("ffill", False):
			results = results.fillna(method="ffill")

		if self.params.get("lag", None) is not None:
			results = results.shift(self.params["lag"]).dropna(how="all")
		return results


