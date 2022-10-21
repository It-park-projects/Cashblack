import requests
url = "http://91.204.239.44/broker-api/send"
params = {
 "messages":
 [
 {
  "recipient":"+998997090576",
  "message-id":"abc000000001",

     "sms":{

       "originator": "3700",
     "content": {
      "text": "Salom"
      }
      }
         }
     ]
}
username = "assistant"
password = "rA@8e3vE)@3X"
response = requests.post(url, auth=(username, password), json=params)
data = response.json()
  
# print(data)s

# print(request.status_code)
# print(request.json())

# response = requests.post(url, auth=(username, password))
# headers = {"Authorization": f"Bearer {response}"}
# print(response.status_code)
# print(response.json())