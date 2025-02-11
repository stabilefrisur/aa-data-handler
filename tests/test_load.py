import pandas as pd
from save import save
from load import load
import pytest

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })

def test_load_csv(sample_dataframe, tmp_path):
    save(sample_dataframe, 'data', 'csv', tmp_path)
    loaded_df = load('data', 'csv', tmp_path)
    pd.testing.assert_frame_equal(sample_dataframe, loaded_df)

def test_load_xlsx(sample_dataframe, tmp_path):
    save(sample_dataframe, 'data', 'xlsx', tmp_path)
    loaded_df = load('data', 'xlsx', tmp_path)
    pd.testing.assert_frame_equal(sample_dataframe, loaded_df)

def test_load_pickle(sample_dataframe, tmp_path):
    save(sample_dataframe, 'data', 'pickle', tmp_path)
    loaded_df = load('data', 'pickle', tmp_path)
    pd.testing.assert_frame_equal(sample_dataframe, loaded_df)
