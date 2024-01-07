# twilio_communication.py
from twilio.rest import Client

# Your Twilio credentials
account_sid = 'AC42057a4d2a65c5fe89fff37c00513358'
auth_token = 'c02592375d0e3f40387477a9e2f57b65'
twilio_number = '+19208439171'  # Your Twilio phone number

# Initialize the Twilio client
client = Client(account_sid, auth_token)

def send_sms(body, to):
    """
    Sends an SMS to a given phone number.
    :param body: String with the message to send.
    :param to: String with the recipient's phone number.
    """
    try:
        message = client.messages.create(
            body=body,
            from_=twilio_number,
            to=to
        )
        print(f"Message sent with SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        if hasattr(e, 'uri'):
            print(f"More information: {e.uri}")


if __name__ == "__main__":
    # Test sending an SMS - replace '+1234567890' with a real number for actual testing
    send_sms("Hello from Twilio!", "+1234567890")
