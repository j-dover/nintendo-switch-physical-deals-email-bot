import boto3
import os
import praw
import json
from Credentials import Credentials


def find_nintendo_switch_physical_deals(app_client_id, app_client_secret, app_user_agent, old_deals):
  new_deals = []

  # Create Reddit Instance to interact with Reddit API
  reddit = praw.Reddit(
      client_id=app_client_id,
      client_secret=app_client_secret,
      user_agent=app_user_agent,
  )
  subreddit = reddit.subreddit("NintendoSwitchDeals")

  # Check the ten newest posts from r/NintendoDeals
  # Filter for new physical deals in the US
  for submission in subreddit.new(limit=10):
    if submission.id not in old_deals and submission.link_flair_text == "Physical Deal" and "/US" in submission.title:
      submission_creation_date = submission.created_utc
      submission_creation_date = datetime.fromtimestamp(submission_creation_date)
      print(f'{submission.title}, created {submission_creation_date}')

      # Add the submission to the new deals list
      new_deals.append(submission)

  return new_deals


def lambda_handler(event, context):
  # Get credential parameters from Systems Manager Parameter Store
  AWS_REGION = os.environ.get('AWS_REGION')
  aws_client = boto3.client('ssm', region_name=AWS_REGION)
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

  # Get new physical deals from r/NintendoSwitchDeals
  client_id = credentials.get_client_id()
  client_secret = credentials.get_client_secret()
  user_agent = credentials.get_user_agent()
  new_deals = find_nintendo_switch_physical_deals(client_id, client_secret, user_agent, old_deals)

  # If new deals list is not empty:
  if new_deals:
    # Add new deals to email body text for non-HTML email clients
    body_text = "Nintendo Switch Physical Deals Email Bot presents:\r\n"
    for submission in new_deals:
      deal_link = f'{submission.url}\r\n'
      body_text += deal_link
    print("Body Text:")
    print(body_text)

    # Add new deals to HTML email body
    html_deals = ""
    for submission in new_deals:
      deal = f'<a href="{submission.url}">{submission.title}</a><br>'
      html_deals += deal

    body_html = """<html>
    <head></head>
    <body style="font-family: Verdana, sans-serif">
      <h1>Nintendo Switch Physical Deals Email Bot presents:</h1><br>
      <p>
        {}
      </p>
    </body>
    </html>
    
    """.format(html_deals)
    print("Body HTML:")
    print(body_html)

    # Set email credentials
    SENDER = credentials.get_email_sender()
    RECIPIENT = credentials.get_email_recipient()
    SUBJECT = "New from r/NintendoSwitchDeals!"
    CHARSET = "UTF-8"

    # Send email with SES SDK and return json with email id if sent successfully
    # Code modified from "Sending email through Amazon SES using an AWS SDK" by Amazon Simple Email Service Developer Guide
    # https://docs.aws.amazon.com/ses/latest/dg/send-an-email-using-sdk-programmatically.html
    aws_client = boto3.client('ses',region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as error:
        print(error.response['Error']['Message'])
        return {
            'statusCode': 400,
            'body': json.dumps(e.response['Error']['Message'])
        }
    else:
        message_id = response['MessageId']
        print(f"Email sent to {SENDER}! Message ID: {message_id}"),
        return {
            'statusCode': 200,
            'body': json.dumps(f"Email sent to {SENDER}! Message ID: {message_id}")
        }
  else:
    # Notify no new deals, no email sent
    print("There are 0 new deals. Thus, no email was sent to user.")

    # Return success json
    return {
        'statusCode': 200,
        'body': json.dumps('No new deals!')
    }