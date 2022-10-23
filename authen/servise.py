import requests



def send_message(username,item):
    url = "http://91.204.239.44/broker-api/send"
    params = {
                "messages":
                     [
                     {
                      "recipient":f"{username}",
                      "message-id":"abc000000001",
                         "sms":{
                         "originator": "3700",
                         "content": {
                          "text": f"Tasdiqlash kodi {item}"
                          }
                          }
                             }
                         ]
                    }
    username = "assistant"
    password = "rA@8e3vE)@3X"
    response = requests.post(url, auth=(username, password), json=params)