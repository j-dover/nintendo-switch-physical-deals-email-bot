import boto3
import os
import praw
from datetime import datetime
from dotenv import load_dotenv,find_dotenv

cache = []

def lambda_handler(event, context):
  # Get today's date
  current_date = date.today()

  # Create Read-Only Reddit Instance
  reddit = praw.Reddit(
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      user_agent=USER_AGENT,
  )

  subreddit = reddit.subreddit("NintendoSwitchDeals")
  
  # Get newest 25 posts from r/NintendoDeals
  # Filter for physical deals
  for submission in subreddit.new(limit=25):
    if submission.link_flair_text == 'Physical Deal':
      print(submission.title)
      time=submission.created_utc
      print(datetime.fromtimestamp(time))
      




  # Return response
  return {
      'statusCode': 200,
      'body': json.dumps('Hello from Lambda!')
  }
