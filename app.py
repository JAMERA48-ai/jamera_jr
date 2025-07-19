from flask import Flask, request, Response, Request
import requests
import asyncio
import httpx
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import threading

# تعطيل تحذيرات SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# هنا توكنات نتاعك
SPAM_TOKENS = [
    ("4039167739", "97145262D0FF42440C62E1BD6EEDE5E3DEBF1ADF3201376AE313A4D5B5DD0538"),
]

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
    dec = [f"{i:02x}" for i in range(128, 256)]
    xxx = [f"{i:02x}" for i in range(1, 128)]
    x = x / 128
    if x > 128:
        x = x / 128
        if x > 128:
            x = x / 128
            if x > 128:
                x = x / 128
                y = (x - int(x)) * 128
                z = (y - int(y)) * 128
                n = (z - int(z)) * 128
                m = (n - int(n)) * 128
                return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]
            else:
                y = (x - int(x)) * 128
                z = (y - int(y)) * 128
                n = (z - int(z)) * 128
                return dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

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
    yield "By API: @@lnc_tomo\n"
    yield "https://t.me/lnctomo"
    thread = threading.Thread(target=send_requests_in_background, args=(id,))
    thread.start()

@app.route('/spam')
def index():
    id = request.args.get('id')
    if id:
        return Response(generate(id), content_type='text/plain')
    else:
        return "Please provide a valid ID."

# هذه الدالة الخاصة بـ vercel أو cloud function
def handler(request: Request):
    return app(request.environ, start_response=lambda status, headers: None)
