
import urllib
import urllib2
import hashlib
import hmac
import binascii
import requests
import json

KEY = "ahFkZXZ-amVycnktc2VydmljZXIPCxIJQXBwQWNjZXNzGAEM"
SECRET = "santa loves you"
BASE_PATH = "/api/v1/"
BASE_URL = "http://localhost:9092" + BASE_PATH


def _sign(method, url, params):
    params["_key"] = KEY
    encoded = urllib.urlencode(params)
    query = "&".join((method.upper(), url, encoded))
    encoded += "&_signature=" + urllib.quote(binascii.b2a_base64(
            hmac.new(SECRET, query, hashlib.sha256).digest()))
    return encoded


def verify_access():
    params = {"yay": "other", "second": "yes"}

    url = BASE_URL + "verify_access"
    full_request = url + "?" + _sign("GET", url, params)
    print full_request
    req = urllib2.urlopen(full_request)
    print req.read()
    return req


def post_log_entry():

    data = [
        {"action": "upload_photo"},
        {"action": "run_app", "quantity": 4},
        {"action": "share_picture"}
    ]
    params = {
        "device_id": "ASD90384KDOHDKS",
        "entries": json.dumps(data)
    }

    url = BASE_URL + "logger"
    req = requests.post(url, data=_sign("POST", url, params))
    print req.content
    print req.status_code
    import pdb
    pdb.set_trace()

if __name__ == "__main__":
    verify_access()
    post_log_entry()
