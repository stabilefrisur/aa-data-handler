# AA Data Handler

## Description
AA Data Handler is a Python project designed to handle saving and loading data, considering various data types and file formats.

## Installation
To install the package, run:
```bash
pip install aa-data-handler
```

## Usage
### Saving Data
You can save a DataFrame, Series, dictionary, or Figure to a file using the `save` function:
```python
from pathlib import Path
import pandas as pd
from save import save

# Create a DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# Save the DataFrame to a CSV file
save(df, 'data', 'csv', Path('data'))
```

#### Additional Examples
1. **Save a Series to a Pickle File:**
    ```python
    series = pd.Series([1, 2, 3, 4, 5])
    save(series, 'series_data', 'pickle', Path('data'))
    ```

2. **Save a Dictionary of DataFrames to an Excel File:**
    ```python
    data_dict = {
        'Sheet1': pd.DataFrame({'A': [1, 2], 'B': [3, 4]}),
        'Sheet2': pd.DataFrame({'C': [5, 6], 'D': [7, 8]})
    }
    save(data_dict, 'data_dict', 'xlsx', Path('data'))
    ```

3. **Save a Matplotlib Figure to a SVG File:**
    ```python
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    save(fig, 'figure', 'svg', Path('data'))
    ```

### Loading Data
You can load a DataFrame, Series, or dictionary from a file using the `load` function:
```python
from load import load

# Load the latest file in the log
loaded_df = load(name='data')

# Print the loaded DataFrame
print(loaded_df)
```

#### Arguments for `load`
- `name` (str): The name of the file to load. If not provided, the function will search the log for the latest file.
- `file_format` (str): The format of the file to load. Supported formats are 'csv', 'xlsx', and 'pickle'.
- `file_path` (Path | str): The path to the file. If not provided, the function will search the log for the latest file.
- `log_id` (str): The unique file ID from the log file. If provided, the function will use this to locate the file.

#### Examples
1. **Load by Name:**
    ```python
    loaded_df = load(name='data')
    ```

2. **Load by Name and Format:**
    ```python
    loaded_df = load(name='data', file_format='csv')
    ```

3. **Load by Name, Format, and Path:**
    ```python
    loaded_df = load(name='data', file_format='csv', file_path='data')
    ```

4. **Load by Log ID:**
    ```python
    loaded_df = load(log_id='unique-log-id')
    ```

## Contributing
No need to contribute here, but thank you!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
