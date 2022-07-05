import json

class Credentials:
    
  def __init__(self, response_parameters):
    self.credential_params = {}

    for parameter in response_parameters:
      name = parameter['Name']
      self.credential_params[name] = parameter['Value']