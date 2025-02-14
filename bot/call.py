from twilio.rest import Client

account_sid = ""
auth_token = ""
twilio_phone_number = ""  
receiver_phone_number = "" 

client = Client(account_sid, auth_token)


def make_tts_call(message):

    try:
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to=receiver_phone_number,
            from_=twilio_phone_number,
            twiml=f"<Response><Say voice='alice'>{message}</Say></Response>"
        )

        print(f"Call initiated successfully. Call SID: {call.sid}")
        return call.sid

    except Exception as e:
        print(f"Error making call: {e}")
        return None
