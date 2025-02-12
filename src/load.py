import pandas as pd
import pickle
from pathlib import Path
from logger import get_action_logger
import os
import re

# General logger for actions
action_logger = get_action_logger('action_logger')

def load(      
        file_name: str = None, 
        file_format: str = None, 
        full_file_path: Path | str = None, 
        log_id: str = None
        ) -> pd.DataFrame | pd.Series | dict | None:
    """Load a DataFrame, Series, or dictionary from a file.

    Args:
        file_name (str): File name without extension.
        file_format (str): File format. Supported formats are 'csv', 'xlsx', and 'pickle'.
        full_file_path (Path | str): Full file path including the file name and extension.
        log_id (str): Unique file ID from the log file.

    Returns:
        pd.DataFrame | pd.Series | dict | None: Loaded object.

    Raises:
        ValueError: If the format is not supported.
        FileNotFoundError: If the specified path does not exist.
    """
    log_entries = _read_log_entries()

    if full_file_path:
        return _load_from_full_path(full_file_path)
    elif file_name or file_format:
        return _load_from_name_and_format(log_entries, file_name, file_format)
    elif log_id:
        return _load_from_log_id(log_entries, log_id)
    else:
        raise ValueError("Insufficient parameters provided for loading the file.")

def _load_from_full_path(full_path):
    if os.path.exists(full_path):
        return _load_file(full_path)
    else:
        raise FileNotFoundError(f"The file {full_path} does not exist.")

def _load_from_name_and_format(log_entries, file_name, file_format):
    pattern = re.compile(file_name) if file_name else None
    matches = [
        entry for entry in log_entries 
        if (not pattern or pattern.search(Path(entry['full_path']).stem)) 
        and (not file_format or entry['file_format'] == file_format)
    ]
    if matches:
        return _load_file(matches[-1]['full_path'])  # Return only the latest match
    else:
        raise FileNotFoundError("No matching file found in the log.")

def _load_from_log_id(log_entries, log_id):
    for entry in reversed(log_entries):
        if entry['log_id'] == log_id:
            return _load_file(entry['full_path'])
    raise FileNotFoundError(f"No file found with log_id {log_id}.")

def _load_file(full_path):
    path = Path(full_path)
    file_format = path.suffix[1:]  # Remove the leading dot
    action_logger.info(f"Loading {file_format} from {full_path}")

    if file_format == 'csv':
        return pd.read_csv(full_path)
    elif file_format == 'xlsx':
        return _load_excel(full_path)
    elif file_format == 'pickle':
        with open(full_path, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unsupported format: {file_format}")

def _read_log_entries():
    log_entries = []
    with open('file_log.log', 'r') as log_file:
        for line in log_file:
            log_id, timestamp, full_path = line.strip().split(',')
            full_path = Path(full_path)
            file_format = full_path.suffix[1:]  # Remove the leading dot
            log_entries.append({
                'log_id': log_id,
                'timestamp': timestamp,
                'full_path': str(full_path),
                'file_format': file_format
            })
    return log_entries

def _load_excel(full_path: Path) -> pd.DataFrame | dict:
    excel_data = pd.read_excel(full_path, sheet_name=None)
    action_logger.info(f"Excel file loaded from {full_path}")
    if len(excel_data) == 1:
        return next(iter(excel_data.values()))
    return excel_data
