import pandas as pd
import pickle
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def load(      
        name: str, 
        format: str, 
        path: Path | str
        ):
    """Load a DataFrame, Series, or dictionary from a file.

    Args:
        name (str): File name.
        format (str): File format. Supported formats are 'csv', 'xlsx', and 'pickle'.
        path (Path | str): File path.

    Returns:
        pd.DataFrame | pd.Series | dict: Loaded object.

    Raises:
        ValueError: If the format is not supported.
        FileNotFoundError: If the specified path does not exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"The specified path does not exist: {path}")
    extension = 'p' if format == 'pickle' else format
    full_path = path / f"{name}.{extension}"
    logging.info(f"Loading {format} from {full_path}")
    
    if format == 'csv':
        return pd.read_csv(full_path)
    elif format == 'xlsx':
        return _load_excel(full_path)
    elif format == 'pickle':
        with open(full_path, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unsupported format: {format}")

def _load_excel(full_path: Path):
    excel_data = pd.read_excel(full_path, sheet_name=None)
    logging.info(f"Excel file loaded from {full_path}")
    if len(excel_data) == 1:
        return next(iter(excel_data.values()))
    return excel_data
