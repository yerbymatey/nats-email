# nats channel emails.ready that notifies emailer service that the email is ready to be sent
#recevie message on emails.ready that willh have ID of the email in the email 
# we'll fetch the email from the database and send it

import asyncio
import asyncpg
import nats.aio.client as NATS
import json
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(email):
    print(email)
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    to = email["to"].split(",")
    cc = email["cc"].split(",")
    mail = Mail(
        to_email=email["from"],
        subject=email['subject'],
        content=sendgrid.Content("text/plain", email['content']),
        mail=sendgrid.Mail(from_email, cc, to, content)
        )
    print(mail)
    response = sg.send(mail)
    return response

async def run():
    nc = NATS()
    await nc.connect(servers=["nats://127.0.0.1:4222"])
    js = nc.jetstream()
    
    async def message_handler(msg):
        email_id = msg.data.decode()
        print(f"got message on emails.ready", )
        conn = await asyncpg.connect(os.environ.get('DATABASE_URL'))
        email = await conn.fetchrow('SELECT \"to\", cc, bcc \"from\", body FROM emails WHERE email_id = $1', email_id)
        if email:
            response = send_email(email)
            print(response)
        else:
            print(f"no email with id {email_id}")
        
        await conn.close()
        
        
        print("listening for emails to send")
        msg.ack()
        
    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(loop))
        loop.run_forever()
        

