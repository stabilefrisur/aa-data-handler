import pandas as pd
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)

def save(
        obj: pd.DataFrame | pd.Series | dict | plt.Figure, 
        name: str, 
        format: str, 
        path: Path | str
        ):
    """Save a DataFrame, Series, dictionary, or Figure to a file.

    Args:
        obj (pd.DataFrame | pd.Series | dict | plt.Figure): Object to save.
        name (str): File name.
        format (str): File format. Supported formats are 'csv', 'xlsx', 'pickle', 'png', and 'svg'.
        path (Path | str): File path.

    Raises:
        TypeError: If the object type is not supported.
        ValueError: If the format is not supported.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)  # Ensure the path exists
    extension = 'p' if format == 'pickle' else format
    full_path = path / f"{name}.{extension}"
    
    logging.info(f"Saving {type(obj).__name__} as {format} to {full_path}")

    if isinstance(obj, pd.DataFrame):
        _save_dataframe(obj, full_path, format)
    elif isinstance(obj, pd.Series):
        _save_series(obj, full_path, format)
    elif isinstance(obj, dict):
        _save_dict(obj, full_path)
    elif isinstance(obj, plt.Figure):
        _save_figure(obj, full_path, format)
    else:
        raise TypeError("Unsupported object type")

def _save_dataframe(df: pd.DataFrame, full_path: Path, format: str):
    if format == 'csv':
        df.to_csv(full_path, index=False)
    elif format == 'xlsx':
        df.to_excel(full_path, index=False)
    elif format == 'pickle':
        with open(full_path, 'wb') as f:
            pickle.dump(df, f)
    else:
        raise ValueError(f"Unsupported format for DataFrame: {format}")
    
    logging.info(f"DataFrame saved to {full_path}")

def _save_series(series: pd.Series, full_path: Path, format: str):
    if format == 'csv':
        series.to_csv(full_path, index=False)
    elif format == 'xlsx':
        series.to_frame().to_excel(full_path, index=False)
    elif format == 'pickle':
        with open(full_path, 'wb') as f:
            pickle.dump(series, f)
    else:
        raise ValueError(f"Unsupported format for Series: {format}")
    
    logging.info(f"Series saved to {full_path}")

def _save_dict(d: dict, full_path: Path):
    if all(isinstance(v, (pd.DataFrame, pd.Series, dict)) for v in d.values()):
        with pd.ExcelWriter(full_path) as writer:
            for key, value in d.items():
                if isinstance(value, pd.DataFrame):
                    value.to_excel(writer, sheet_name=key, index=False)
                elif isinstance(value, pd.Series):
                    value.to_frame().to_excel(writer, sheet_name=key, index=False)
                elif isinstance(value, dict):
                    nested_path = full_path.parent / f"{key}.xlsx"
                    _save_dict(value, nested_path)
    else:
        raise ValueError("All values in the dictionary must be DataFrame, Series, or nested dictionaries")
    
    logging.info(f"Dictionary saved to {full_path}")

def _save_figure(fig: plt.Figure, full_path: Path, format: str):
    if format in ['png', 'svg']:
        fig.savefig(full_path)
    else:
        raise ValueError(f"Unsupported format for Figure: {format}")
    
    logging.info(f"Figure saved to {full_path}")
