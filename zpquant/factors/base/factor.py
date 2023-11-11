"""This module sets the config for any equity factor """

__author__ = "deepak"
__email__ = "deepaksinghcws@gmail.com"
__all__ = ['EquityFactor']

import pandas as pd
import numpy as np
from zpmeta.superclasses.panelcachedsource import PanelCachedSource
from zpmeta.superclasses.functionclass import FunctionClass
from zpmeta.metaclasses.singletons import MultitonMeta


class Factor(PanelCachedSource, metaclass=MultitonMeta):
	"""
	

	"""
	def __init__(self, params: dict = None):
        """
        Standard parameters for the function class.
        params: dict
            seed: int
                The seed for the random number generator.
            freq: str
                The frequency of the output weights.
            distribution: callable
                Numpy distribution function wrapped in functools partial, default is standard normal distribution.
        """
        super(Factor, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)

	
    # ask ramanuj
	def _execute(self, call_type=None, entities=None, period=None):
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
		#portfolio.signal
		self.run_main(period, universe)
		self.check_consistency()
		self.value = self.value.reindex(pd.date_range(period[0], period[1], freq="D"))

		if "ffill" in self.params.keys() and self.params["ffill"]:
			self.value = self.value.fillna(method="ffill")

		self.value = self.value.replace(0, np.nan)
		self.value = self.value.shift(self.params["lag"]).dropna(how="all")
		# return self


