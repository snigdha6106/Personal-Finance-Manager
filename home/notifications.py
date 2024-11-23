from django.conf import settings
from twilio.rest import Client
def send_sms_notification(to, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
        print("SMS sent successfully.")
    except Exception as e:
        print(f"Error sending SMS: {e}")
