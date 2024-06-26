Email Processing and Sending Service
This project consists of two main components: an email processing service and an email sending service. These services work together to handle email requests, process them using AI, store the details in a database, and finally send the emails.
Table of Contents

Features
Requirements
Installation
Usage
Configuration
Components

Features

Listen for new email specifications via NATS
Process natural language prompts using OpenAI's GPT model
Extract email details from the processed prompts
Store email details in a PostgreSQL database
Send emails using SendGrid
Asynchronous operation for improved performance

Requirements

Python 3.7+
NATS Server
PostgreSQL database (Neon)
OpenAI API key
SendGrid API key

Installation

Clone the repository:
Copygit clone https://github.com/yourusername/email-processing-service.git
cd email-processing-service

Install the required packages:
Copypip install nats-py asyncio openai psycopg2-binary sendgrid

Set up your environment variables:
Copyexport DATABASE_URL="your_postgres_connection_string"
export SENDGRID_API_KEY="your_sendgrid_api_key"
export OPENAI_API_KEY="your_openai_api_key"


Usage

Start the NATS server.
Run the email processing service:
Copypython email_processor.py

Run the email sending service:
Copypython email_sender.py


Configuration

Adjust the NATS server address in both scripts if needed (default is "nats://127.0.0.1:4222").
Modify the OpenAI model in the generate_email_details function if desired.
Customize the database schema and SQL queries as needed.

Components
Email Processor (email_processor.py)
This script:

Connects to NATS and listens for new email specifications
Processes the specifications using OpenAI's GPT model
Extracts email details from the processed output
Stores the extracted details in the PostgreSQL database

Email Sender (email_sender.py)
This script:

Listens for messages on the "emails.ready" NATS channel
Retrieves email details from the database based on the received email ID
Sends the email using SendGrid

Paper Downloader (paper_downloader.py)
This additional script:

Connects to NATS and listens for new paper URLs
Downloads PDF papers from the provided URLs
Stores paper information in a PostgreSQL database
Publishes a message when a paper is successfully downloaded