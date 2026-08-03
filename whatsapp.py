from twilio.rest import Client
import config


client = Client(
    config.ACCOUNT_SID,
    config.AUTH_TOKEN
)



def send_whatsapp(image_url):

    try:

        message = client.messages.create(

            body=
            "🚨 AI Security System\n"
            "Unknown person detected!",


            from_=
            config.FROM_WHATSAPP,


            to=
            config.TO_WHATSAPP,


            media_url=[
                image_url
            ]

        )


        print(
            "WhatsApp sent"
        )


    except Exception as e:

        print(
            "WhatsApp error:",
            e
        )