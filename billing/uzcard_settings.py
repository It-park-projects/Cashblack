import requests
import json
import base64

usrPass = "texnolike:myuU3te4N01!KE"
data_bytes = usrPass.encode("utf-8")
b64Val = base64.b64encode(data_bytes)


def create_user_card(amount,card_number,expire_date,user_id,):
    url = "https://pay.myuzcard.uz/api/Payment/paymentWithoutRegistration"
    token = b64Val
    payload = json.dumps({
        "amount": f"{amount}",
        "cardNumber": f"{card_number}",
        "expireDate": f"{expire_date}",
        "extraId": f"{user_id}"

    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic'+" "+token.decode('utf-8'),
        'Content-Type': 'application/json'
    }
    print(headers)

    response = requests.request("POST",url,  headers=headers, data=payload)

    print(response.text)

def confirmUserCard(response,code):
    url = 'https://pay.myuzcard.uz/api/Payment/confirmPayment'
    payload = json.dumps({
        "session": 17437751,
        "otp": "750309"
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic dGV4bm9saWtlOm15dVUzdGU0TjAxIUtF',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)


 


# url_create_card_user = "https://pay.myuzcard.uz/api/UserCard/createUserCard"
# url_confirm_card = "https://pay.myuzcard.uz/api/UserCard/confirmUserCardCreate"


