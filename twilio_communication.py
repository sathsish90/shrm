# twilio_communication.py
from twilio.rest import Client

# Your Twilio credentials
account_sid = '{}'
auth_token = '{}'
twilio_number = '{}'  # Your Twilio phone number

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
