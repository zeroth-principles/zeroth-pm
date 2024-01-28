
from functools import partial
import numpy as np
import pytest
import pandas as pd
from zpquant.features.momentum.price_momentum import PriceMomentum_g_Returns, EQPriceMomentum, FUPriceMomentum
from zputils.dataframes.simulated import SimulatedDataFrame
from datetime import datetime

@pytest.fixture
def sample_data():
    # Create a sample DataFrame for testing
    rr = SimulatedDataFrame(params = dict(seed = 0, freq = "B", distribution = partial(np.random.normal, loc = 0.0, scale = 0.05)))
    result = rr(entities=['AAPL', 'GOOGL', 'META'], period=('2022-01-01', '2022-01-30'))
    return pd.DataFrame(result)

def test_PriceMomentum_g_Returns(sample_data):
    # Create an instance of PriceMomentum_g_Returns
    pm = PriceMomentum_g_Returns(params = dict(lookback_period = 15, axis=0))

    # Execute the function
    result = pm(operand=sample_data)

    # Assert the result
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 6

def test_EQPriceMomentum():
    # Create an instance of EQPriceMomentum
    eq_pm = EQPriceMomentum(params = dict(lookback_period = 15, axis=0, simulation = True))

    # Execute the function
    result = eq_pm(entities=['AAPL', 'GOOG'], period=(datetime(2022, 1, 1), datetime(2022, 1, 30)))

    # Assert the result
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 30

def test_FUPriceMomentum():
    # Create an instance of FUPriceMomentum
    fu_pm = FUPriceMomentum(params = dict(lookback_period = 15, axis=0, simulation = True))

    # Execute the function
    result = fu_pm(entities=['ES', 'NQ'], period=(datetime(2022, 1, 1), datetime(2022, 1, 30)))

    # Assert the result
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 30
