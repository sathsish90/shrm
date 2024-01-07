# csv_handler.py
import pandas as pd

def load_csv_data(file_path):
    """
    Loads data from a CSV file into a DataFrame.
    :param file_path: String with the path to the CSV file.
    :return: DataFrame with the loaded data.
    """
    df = pd.read_csv(file_path)
    return df

def main():
    # Load the data
    df = load_csv_data("ThyroidDF.csv")
    print(df.head())

if __name__ == "__main__":
    main()
