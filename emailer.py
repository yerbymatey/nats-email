fromimport nats
import asyncio
import OpenAI
import psycopg2
import json

# Function to initialize the NATS connection and listen for new email specs
async def listen_for_emails():
    # Connect to the NATS server
    nc = await nats.connect("nats://127.0.0.1:4222")
    js = nc.jetstream()

    # Define the message handler
    async def message_handler(msg):
        subject, reply, data = msg.subject, msg.reply, msg.data.decode()
        print(f"Received a message on '{subject}': {data}")

        # Extract details from the natural language prompt
        prompt = f"Extract details for an email: to, cc, bcc, from, body, initial prompt, shortened spec, audience, context knowledge from the following spec: '{data}'"
        extracted_details = await generate_email_details(prompt)

        # Insert the details into the Neon database
        await insert_email_details(json.loads(extracted_details))

    # Subscribe to the 'emails.new_email' subject
    await js.subscribe("emails.new_email", cb=message_handler, config=ConsumerConfig(deliver_policy=DeliverPolicy.NEW))

# Function to use an LLM for processing the natural language prompt
async def generate_email_details(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # Adjust as needed for the current available model
        prompt=prompt,
        max_tokens=1024
    )
    return response.choices[0].text

# Function to insert extracted email details into the database
async def insert_email_details(details):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    # Construct SQL query to insert the extracted details into the Emails table
    sql = """
    INSERT INTO Emails (to, cc, bcc, from, body, initial_prompt, shortened_spec, audience, context_knowledge)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(sql, (
        details['to'], details['cc'], details['bcc'], details['from'],
        details['body'], details['initial_prompt'], details['shortened_spec'],
        details['audience'], details['context_knowledge']
    ))
    conn.commit()
    cur.close()
    conn.close()

# Main execution block
if __name__ == "__main__":
    asyncio.run(listen_for_emails())