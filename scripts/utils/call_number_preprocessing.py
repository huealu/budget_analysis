"""
"""
import pandas as pd


############################## Extract Call Number #############################

def extract_call_number(df: pd.DataFrame, call_number_column: str) -> pd.DataFrame:
    """
    Extract the call number from the specified column in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the call number column.
        call_number_column (str): The name of the column containing the call numbers.

    Returns:
        pd.DataFrame: A DataFrame with an additional column for the extracted call numbers.
    """
    # Create a new column for the extracted call numbers
    df['Extracted_Call_Number'] = df[call_number_column].apply(lambda x: str(x).split()[0] if pd.notnull(x) else None)

    return df

