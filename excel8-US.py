#New twilio details updated

import pandas as pd
import os
from twilio.rest import Client

# Twilio configuration
account_sid = 'AC317330a10b601553c8a23c489011d519'
auth_token = 'b1589df7cb5cff4e73d9b3ba20ddb4ef'
twilio_number = '+18884820408'
client = Client(account_sid, auth_token)

# Columns to monitor for changes
columns_to_monitor = ['age', 'sex', 'on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_meds', 
                      'sick', 'pregnant', 'thyroid_surgery', 'I131_treatment', 'query_hypothyroid', 
                      'query_hyperthyroid', 'lithium', 'goitre', 'tumor', 'hypopituitary', 'psych', 
                      'TSH_measured', 'TSH', 'T3_measured', 'T3', 'TT4_measured', 'TT4', 
                      'T4U_measured', 'T4U', 'FTI_measured', 'FTI', 'TBG_measured', 'TBG']

# Function to send a text message
def send_text_message(patient_id, mobile_number, changes):
    formatted_number = f'+1{mobile_number}'
    message_body = f"Hi {patient_id}, Your medical record has been updated:\n" + "\n".join(changes)
    try:
        message = client.messages.create(
            to=formatted_number, 
            from_=twilio_number,
            body=message_body
        )
        print(f"Message sent to {patient_id}: {message.sid}")
    except Exception as e:
        print(f"Error sending message to {patient_id}: {e}")

# Function to check for updates in the Excel file
def check_for_updates(current_data, last_data):
    updates_found = False
    for patient_id, current_row in current_data.iterrows():
        if patient_id in last_data.index:
            old_row = last_data.loc[patient_id]
            changes = []
            for col in columns_to_monitor:
                if str(old_row[col]) != str(current_row[col]):
                    changes.append(f"{col} updated from {old_row[col]} to {current_row[col]}")

            if changes:
                send_text_message(patient_id, current_row['mobile_number'], changes)
                updates_found = True

    return updates_found

# Read the current data and the processed updates
current_data = pd.read_csv('ThyroidDF.csv').set_index('patient_id')
last_data = pd.DataFrame()
if 'processed_updates.csv' in os.listdir():
    last_data = pd.read_csv('processed_updates.csv').set_index('patient_id')

# Check for updates and update the processed log
updates_found = check_for_updates(current_data, last_data)
if updates_found:
    # Update processed log only if there were updates
    current_data.to_csv('processed_updates.csv')
else:
    print("No new patient information updates found")
