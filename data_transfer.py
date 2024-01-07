# data_transfer.py
import pandas as pd
import re
from twilio_communication import send_sms

def fetch_patient_data(patient_id, df):
    """
    Fetches patient data from the dataframe based on the patient_id.
    :param patient_id: Integer with the patient's ID.
    :param df: DataFrame containing patient data.
    :return: DataFrame with the patient's data.
    """
    patient_data = df[df['patient_id'] == patient_id]
    return patient_data

def format_to_e164(raw_number, country_code='+91'):
    """
    Formats a raw phone number to E.164 format.
    :param raw_number: Integer or String, the raw phone number.
    :param country_code: String, the country code to prepend.
    :return: String, the formatted phone number.
    """
    number = str(raw_number)
    if not number.startswith('+'):
        number = country_code + number
    return number

def validate_phone_number(number):
    """
    Validates that the phone number is in E.164 format.
    :param number: String with the phone number.
    :return: Boolean indicating if the number is valid.
    """
    if pd.isna(number):  # Check for NaN values
        return False
    number = str(number)  # Ensure the number is treated as a string
    pattern = re.compile(r"^\+[1-9]\d{1,14}$")
    return pattern.match(number) is not None

def main():
    print("Loading data...")
    df = pd.read_csv("ThyroidDF.csv")  # Ensure the path to your CSV is correct
    
    print("Available Patient IDs:", df['patient_id'].tolist())
    
    input_id = input("Enter the Patient ID: ")

    try:
        patient_id = int(input_id)
    except ValueError:
        print(f"The entered Patient ID '{input_id}' is not a valid integer.")
        return
    
    print(f"Fetching data for Patient ID: {patient_id}")
    patient_data = fetch_patient_data(patient_id, df)
    
    if patient_data.empty:
        print(f"No data found for patient ID {patient_id}")
        return
    
    phone_column_name = 'mobile_number'  # Replace with the actual column name in your CSV
    if phone_column_name not in df.columns:
        print(f"The column '{phone_column_name}' does not exist in the data.")
        return
    
    if len(patient_data[phone_column_name].values) == 0 or pd.isna(patient_data[phone_column_name].values[0]):
        print(f"No phone number available for patient ID {patient_id}")
        return
    
    raw_phone_number = patient_data[phone_column_name].values[0]
    phone_number = format_to_e164(raw_phone_number)
    
    if not validate_phone_number(phone_number):
        print(f"The phone number {raw_phone_number} is not in a valid E.164 format.")
        return
    
    patient_details = str(patient_data.iloc[0])  # Convert the first row of patient data to string
    print(f"Sending SMS with patient details to {phone_number}: {patient_details}")
    
    # Sending the SMS
    send_sms(patient_details, phone_number)

if __name__ == "__main__":
    main()
