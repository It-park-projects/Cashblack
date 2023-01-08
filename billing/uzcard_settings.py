import requests
import json
import base64

usrPass = "texnolike:myuU3te4N01!KE"
data_bytes = usrPass.encode("utf-8")
b64Val = base64.b64encode(data_bytes)


# def create_user_card(amount,card_number,expire_date,user_id,):
#     url = "https://pay.myuzcard.uz/api/Payment/paymentWithoutRegistration"
#     token = b64Val
#     payload = json.dumps({
#         "amount": f"{amount}",
#         "cardNumber": f"{card_number}",
#         "expireDate": f"{expire_date}",
#         "extraId": f"{user_id}"

#     })
#     headers = {
#         'Accept': 'application/json',
#         'Authorization': 'Basic'+" "+token.decode('utf-8'),
#         'Content-Type': 'application/json'
#     }
#     response = requests.request("POST",url,  headers=headers, data=payload)
#     res = json.loads(response.text)

def confirmUserCard(res,otp):
    token = b64Val
    url = 'https://pay.myuzcard.uz/api/Payment/confirmPayment'
    payload = json.dumps({
        "session": f"{res}",
        "otp": f"{otp}"
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic'+" "+token.decode('utf-8'),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)



 


# url_create_card_user = "https://pay.myuzcard.uz/api/UserCard/createUserCard"
# url_confirm_card = "https://pay.myuzcard.uz/api/UserCard/confirmUserCardCreate"


