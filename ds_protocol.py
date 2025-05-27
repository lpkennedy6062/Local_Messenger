# ds_protocol.py
# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python
# Replace the following placeholders with your information.
# Liam
# lpkenned@uci.edu
# 81845142

import json
from collections import namedtuple

ServerResponse = namedtuple('ServerResponse', ['type','message', 'token', 'messages'])

def extract_json(json_msg:str) -> ServerResponse:
  '''Call the json.loads function on a json string and convert it to a DataTuple object'''
  try:
    json_obj = json.loads(json_msg)
  except json.JSONDecodeError as e:
    raise ValueError(f"Invalid JSON:{e}")
  if 'response' not in json_obj or not isinstance(json_obj['response'], dict):
    raise ValueError("Missing or invalid 'response' field")
  r = json_obj['response']
  return ServerResponse(type = r.get('type'), message = r.get('message'), token = r.get('token'), messages = r.get('messages'))
  
def make_auth(username: str, password: str) -> str:
  return json.dumps({"authenticate": {"username": username, "password": password}})

def make_directmessage(token: str, entry: str, recipient: str, timestamp: float) -> str:
  return json.dumps({"token": token, "directmessage": {"entry": entry, "recipient": recipient, "timestamp": str(timestamp)}})

def make_fetch(token, what) -> str:
  return json.dumps({"token": token, "fetch": what})


  
