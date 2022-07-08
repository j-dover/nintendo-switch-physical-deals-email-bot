# Nintendo Switch Physical Deals Email Bot
## About
The Nintendo Switch Physical Deals Email Bot consists of an AWS Lambda function that notifies the user with an email when new US deals for physical products are found in r/NintendoSwitchDeals. It obtains data from r/NintendoSwitchDeals by utilizing the [Reddit API](https://www.reddit.com/dev/api).

## Technologies Used:
- Python
- [PRAW](https://praw.readthedocs.io/en/stable/)
- AWS SDK (Boto3)
  - AWS Lambda
  - Amazon SES
  - AWS Systems Manager Parameter Store
