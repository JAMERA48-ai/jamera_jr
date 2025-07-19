from flask import Request

def handler(request: Request):
    return app(request.environ, start_response=lambda status, headers: None)from flask import Flask, request, Response
import requests
import asyncio
import httpx
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#fox هنا توكنات نتاعك
SPAM_TOKENS = [    ("4039167739", "97145262D0FF42440C62E1BD6EEDE5E3DEBF1ADF3201376AE313A4D5B5DD0538"),]

app = Flask(__name__)

retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"],
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

def Encrypt_ID(x):
    x = int(x)
    dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
    xxx = ['1', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']
    x = x / 128
    if x > 128:
        x = x / 128
        if x > 128:
            x = x / 128
            if x > 128:
                x = x / 128
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                m = (n - int(strn)) * 128
                return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]
            else:
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                return dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()
#fox هنا api jwt
def get_jwt(uid, password):
    api_url = f"https://ch9ayfa-jwt.vercel.app/get?uid={uid}&password={password}"
    try:
        response = session.get(api_url, verify=False, timeout=30)
        print(f"API Response: {response.text}")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("token")
            else:
                print(f"Failed to get JWT: {data.get('message', 'Unknown error')}")
                return None
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

async def async_add_fr(id, token):
    url = 'https://clientbp.common.ggbluefox.com/RequestAddingFriend'
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB48',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {token}',
        'Content-Length': '16',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    data = bytes.fromhex(encrypt_api(f'08a7c4839f1e10{Encrypt_ID(id)}1801'))
    
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(url, headers=headers, data=data)
        if response.status_code == 400 and 'BR_FRIEND_NOT_SAME_REGION' in response.text:
            return f'Id : {id} Not In Same Region !'
        elif response.status_code == 200:
            return f'Good Response Done Send To Id : {id}!'
        elif 'BR_FRIEND_MAX_REQUEST' in response.text:
            return f'Id : {id} Reached Max Requests !'
        elif 'BR_FRIEND_ALREADY_SENT_REQUEST' in response.text:
            return f'Token Already Sent Requests To Id : {id}!'
        else:
            return response.text

def send_requests_in_background(id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [async_add_fr(id, get_jwt(uid, pw)) for uid, pw in SPAM_TOKENS]
    responses = loop.run_until_complete(asyncio.gather(*tasks))
    print("All requests sent:", responses)

def generate(id):
    yield f"Sending friend requests to player {id}...\n"
    yield "By API: @BL_RX and @vam_piros\n"
    yield "https://t.me/AMIN_TEAM_2\n"
    thread = threading.Thread(target=send_requests_in_background, args=(id,))
    thread.start()

@app.route('/spam')
def index():
    id = request.args.get('id')
    if id:
        return Response(generate(id), content_type='text/plain')
    else:
        return "Please provide a valid ID."

from flask import Request

def handler(request: Request):
    return app(request.environ, start_response=lambda status, headers: None)
