import json

class Credentials:
  """
  Class that represent credentials 

  Attributes:
  store (dict)
    dictionary containing parameters from AWS Systems Manager Parameter Store 
  """

  def __init__(self, response_parameters):
    """
    Constructor for Credentials

    Parameters:
      response_parameters (list of dict):
      list containing parameters from AWS Systems Manager Parameter Store
    """
    self.__store = {}

    for parameter in response_parameters:
      name = parameter['Name']
      self.__store[name] = parameter['Value']
  
  def get_store(self):
    """
    Returns a dictionary containing key-value pairs that represent the parameters
    and their respective values
    """
    return self.__store
  
  def get_recipient_email(self):
    """
    Returns a string that represents the recipient email address
    """
    return self.__store['email_recipient']

  def get_sender_email(self):
    """
    Returns a string that represents the sender email address
    """
    return self.__store['email_sender']
  
  def get_user_agent(self):
    """
    Returns a string that represents the user agent
    """
    return self.__store['user_agent']
  
  def get_client_id(self):
    """
    Returns a string that represents the client application id for the Reddit API
    """
    return self.__store['client_id']

  def get_client_secret(self):
    """
    Returns a string that represents the client application secret for the Reddit API
    """
    return self.__store['client_secret']