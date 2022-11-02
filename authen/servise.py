import requests



def send_message(username,item,im):
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
                          "text": f"Tasdiqlash kodi {item} bu kodni hechkimga aytmang {im}"
                          }
                          }
                             }
                         ]
                    }
    username = "assistant"
    password = "rA@8e3vE)@3X"
    response = requests.post(url, auth=(username, password), json=params)