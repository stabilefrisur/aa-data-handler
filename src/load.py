import pandas as pd
import pickle
from pathlib import Path
import logging

# General logger for actions
action_logger = logging.getLogger('action_logger')
action_handler = logging.StreamHandler()
action_handler.setLevel(logging.INFO)
action_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
action_handler.setFormatter(action_formatter)
action_logger.addHandler(action_handler)
action_logger.propagate = False  # Disable propagation

def load(      
        name: str = None, 
        file_format: str = None, 
        file_path: Path | str = None, 
        log_id: str = None
        ) -> pd.DataFrame | pd.Series | dict | None:
    """Load a DataFrame, Series, or dictionary from a file.

    Args:
        name (str): File name.
        file_format (str): File format. Supported formats are 'csv', 'xlsx', and 'pickle'.
        file_path (Path | str): File path.
        log_id (str): Unique file ID from the log file.

    Returns:
        pd.DataFrame | pd.Series | dict | None: Loaded object.

    Raises:
        ValueError: If the format is not supported.
        FileNotFoundError: If the specified path does not exist.
    """
    if log_id:
        name, file_format, file_path = _get_file_info_from_log(log_id)
    
    if not file_path or not file_format:
        name, file_format, file_path = _search_file_log(name)
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"The specified path does not exist: {path}")
    extension = 'p' if file_format == 'pickle' else file_format
    full_path = path / f"{name}.{extension}"
    action_logger.info(f"Loading {file_format} from {full_path}")
    
    if '*' in name:
        return _load_files_by_pattern(name, file_format, path)
    
    if file_format == 'csv':
        return pd.read_csv(full_path)
    elif file_format == 'xlsx':
        return _load_excel(full_path)
    elif file_format == 'pickle':
        with open(full_path, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unsupported format: {file_format}")

def _search_file_log(name: str) -> tuple:
    with open('file_log.log', 'r') as log_file:
        for line in log_file:
            _, _, full_path = line.strip().split(',')
            full_path = Path(full_path)
            if name in full_path.stem:
                name = full_path.stem
                file_format = full_path.suffix[1:]  # Remove the leading dot
                file_path = full_path.parent
                return name, file_format, file_path
    raise FileNotFoundError(f"No matching entries found for name: {name}")

def _load_files_by_pattern(pattern: str, file_format: str, file_path: Path) -> list | None:
    path = Path(file_path)
    files = list(path.glob(f"{pattern}.{file_format}"))
    if not files:
        raise FileNotFoundError(f"No files matching pattern {pattern} found in {path}")
    action_logger.info(f"Found {len(files)} files matching pattern {pattern} in {path}")
    loaded_files = [_load_single_file(file, file_format) for file in files]
    if len(loaded_files) == 1:
        return loaded_files[0]
    return loaded_files

def _load_single_file(file: Path, file_format: str) -> pd.DataFrame | pd.Series | dict:
    action_logger.info(f"Loading {file_format} from {file}")
    if file_format == 'csv':
        return pd.read_csv(file)
    elif file_format == 'xlsx':
        return _load_excel(file)
    elif file_format == 'pickle':
        with open(file, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unsupported format: {file_format}")

def _load_excel(full_path: Path) -> pd.DataFrame | dict:
    excel_data = pd.read_excel(full_path, sheet_name=None)
    action_logger.info(f"Excel file loaded from {full_path}")
    if len(excel_data) == 1:
        return next(iter(excel_data.values()))
    return excel_data

def _get_file_info_from_log(id: str) -> tuple:
    with open('file_log.log', 'r') as log_file:
        for line in log_file:
            log_id, _, full_path = line.strip().split(',')
            if log_id == id:
                full_path = Path(full_path)
                name = full_path.stem
                file_format = full_path.suffix[1:]  # Remove the leading dot
                file_path = full_path.parent
                return name, file_format, file_path
    raise FileNotFoundError(f"No entry found for file ID: {id}")
