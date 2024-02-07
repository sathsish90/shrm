from twilio.rest import Client

account_sid = 'AC3d2adbc594735d80b7e7584c03fda93a'
auth_token = '42a0557a566830b4062eabdb368edc12'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+15105009867',
  body='hello, this is a FHIR test message',
  to='+919840969548'
)

print(message.sid)