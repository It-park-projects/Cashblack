import requests
endpoint="http://91.204.239.44/broker-api/send"
data2 = {
    "login":"assistant",
    "password":"rA@8e3vE)@3X"
}
vash_token_zdes=requests.post(endpoint, data=data2).json()['data']['token']
headers = {"Authorization": f"Bearer {vash_token_zdes}"}
data = {
    "mobile_phone": "998942732708",
    "message":"test uchun",
    "from":"4546",
    "callback_url":"http://0000.uz/test.php"
} 
print(requests.post("http://notify.eskiz.uz/api/message/sms/send",data=data, headers=headers).json())