import json

class ParameterList:
    
  def __init__(self, response_parameters):
    self.params = {}

    for parameter in response_parameters:
      name = parameter['Name']
      self.params[name] = parameter['Value']