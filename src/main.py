import pandas as pd
from pathlib import Path
import logging

# Adjust the import statements
from save import save
from load import load

def main():
    logging.basicConfig(level=logging.INFO)
    
    # Create a DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    
    # Save the DataFrame to a CSV file
    save(df, 'data', 'csv', Path('data'))
    
    # Load the CSV file into a DataFrame
    loaded_df = load('data', 'csv', Path('data'))
    
    # Print the loaded DataFrame
    print(loaded_df)

if __name__ == "__main__":
    main()