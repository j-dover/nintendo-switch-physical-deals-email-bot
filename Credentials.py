import json

class Credentials:
    
  def __init__(self, response_parameters):
    self.__store = {}

    for parameter in response_parameters:
      name = parameter['Name']
      self.__store[name] = parameter['Value']
  
  def get_store(self):
    return self.__store
  
  def get_recipient_email(self):
    return self.__store['email_recipient']

  def get_sender_email(self):
    return self.__store['email_sender']
  
  def get_user_agent(self):
    return self.__store['user_agent']
  
  def get_client_id(self):
    return self.__store['client_id']

  def get_client_secret(self):
    return self.__store['client_secret']