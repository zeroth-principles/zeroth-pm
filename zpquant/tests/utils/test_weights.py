"""test_weights file contains test cases for weights util file in zpquant"""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']


import pytest
import pandas as pd
from functools import partial
from zpquant.utils.weights import PPW_g_RW, PPW_g_RW_g_R
import numpy as np
from datetime import datetime
from zpquant.utils.returns import CumulativeReturn_g_AnchorIndex

@pytest.fixture
def sample_weights():
    date_rng = pd.date_range(start='2022-01-01', end='2022-01-10', freq='B')
    weights = pd.DataFrame({'A': np.random.rand(len(date_rng)),
                            'B': np.random.rand(len(date_rng))},
                            index=date_rng)
    return weights

@pytest.fixture
def sample_returns(sample_weights):
    returns = sample_weights.pct_change().fillna(0)
    return returns

def test_ppw_g_rw_basic(sample_weights):
    params = {'BOD': False, 'freq': 'B'}
    dw_g_rw = PPW_g_RW(params)
    result = dw_g_rw(operand= sample_weights)
    expected = sample_weights
    pd.testing.assert_frame_equal(result , expected)

def test_ppw_g_rw_g_r_basic(sample_weights, sample_returns):
    params = {'BOD': True, 'freq': 'B', "return": sample_returns}
    operand = sample_weights

    result =  PPW_g_RW_g_R()(operand=operand, params=params)
    cumulative_ret = CumulativeReturn_g_AnchorIndex()(sample_returns, params = dict(index = sample_weights.index))
    expected = sample_weights.fillna(0).multiply(1 + cumulative_ret)
    expected.loc[sample_weights.index, :] = sample_weights
    expected = expected.shift(1).dropna(how="all", axis=0)
    pd.testing.assert_frame_equal(result, expected)