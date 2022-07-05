import boto3
import os
import praw
from dotenv import load_dotenv,find_dotenv
import json
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

  # Create old deals list for caching data from file
  old_deals = []

  # If old deals file exists: read it and push to old deals list
  file_path = "/tmp/old_deals.txt"
  if os.path.exists(file_path):
    # Read file data and push into old deals list
    try:
      print(f'Reading {file_path}')
      with open(file_path, 'r') as file:
        for submission_id in file:
          old_deals.append(submission_id.strip("\n"))
        
    except OSError as error:
      print(f'Failed to open {file_path}')
      return {
        'statusCode': 500,
        'body': json.dumps(error)
      }

  # Else: Create old deals file
  else: 
    try:
      file = open(file_path, 'a')
      file.close()
      print(f'Created file {file_path}')
    except OSError as error:
      print(f'Failed to create {file_path}')
      return {
        'statusCode': 500,
        'body': json.dumps(error)
      }


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