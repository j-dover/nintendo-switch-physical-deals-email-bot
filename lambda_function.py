import boto3
import os
import praw
from dotenv import load_dotenv,find_dotenv
import Credentials


def lambda_handler(event, context):
  # Get credential parameters from Systems Manager Parameter Store
  aws_client = boto3.client('ssm')
  response = aws_client.get_parameters(
      Names=[
          'email_sender',
          'email_recipient',
          'client_id',
          'client_secret',
          'user_agent'
      ],
      WithDecryption=True
  )

  # Store credential parameters into Credentials object
  credentials = Credentials(response['Parameters'])

  # Create old deals list
  # Create old deals file if it doesn't exist/Open old deals file and push to file
  # Create new deals list
  # Create Reddit Instance
  # Find latest posts in r/NintendoSwitchDeals:
    # If it fits filters: push to new deals list
  # If new deals list is not empty: 
    # Add new deals to email body text
    # Set email credentials
    # Send email and return json with email id if sent successfully
  # Else:
    # Notify no new deals, no email sent
    # Return success json
  

  # Hello World Return response from Lambda:
  # return {
  #     'statusCode': 200,
  #     'body': json.dumps('Hello from Lambda!')
  # }