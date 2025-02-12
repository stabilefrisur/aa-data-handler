import pandas as pd
from pathlib import Path

from logger import get_action_logger
from save import save
from load import load

def main():
    action_logger = get_action_logger('action_logger')
    action_logger.info("Starting main function")
    
    # Create a DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    
    # Save the DataFrame to a CSV file
    save(df, 'data', 'csv', Path('data'))
    
    # Load the latest file in the log
    loaded_df = load(name='data')
    
    # Print the loaded DataFrame
    print(loaded_df)

if __name__ == "__main__":
    main()