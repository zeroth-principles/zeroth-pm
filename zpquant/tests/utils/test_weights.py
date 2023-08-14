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
from zpquant.utils.weights import DW_g_RW
from zputils.dataframe import RandomReturn
import numpy as np

@pytest.fixture
def sample_operand():
    rr = RandomReturn(params={'seed': 0, 'freq': 'W-MON', 'distribution': partial(np.random.uniform, low=0.0, high=1.0)})
    return rr(entities=['Asset1', 'Asset2'], period=('2022-01-01', '2022-01-30'))

def test_dw_g_rw_with_valid_operand(sample_operand):
    func = DW_g_RW()
    result = func(operand=sample_operand)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (15, 2)
    assert 'Asset1' in result.columns
    assert 'Asset2' in result.columns

def test_dw_g_rw_without_operand():
    func = DW_g_RW()
    with pytest.raises(ValueError, match="operand cannot be None!"):
        func(operand=None, period=('2022-01-01', '2022-01-30'))
    
