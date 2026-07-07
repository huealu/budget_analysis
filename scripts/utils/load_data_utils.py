"""
"""

# Import packages
import os
import pandas as pd


############################# Load data function #############################

def load_data(data_path: str, file_name: str) -> pd.DataFrame:
    """
    Load data from a CSV / Excel file.

    Args:
        data_path (str): The path to the directory containing the file.
        file_name (str): The name of the file to load.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    """
    # Construct the full file path
    full_path = os.path.join(data_path, file_name)

    # Determine the file type and load accordingly
    if file_name.endswith('.csv'):
        data = pd.read_csv(full_path)
    elif file_name.endswith(('.xlsx', '.xls')):
        data = pd.read_excel(full_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file!")

    return data


