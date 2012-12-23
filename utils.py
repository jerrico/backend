
import hmac
import hashlib
import binascii
import webapp2
import urllib


key_store = {
    "test_app": "hidden_key",
    "meinzwo": "herforder weihnacht"
}


def verify_request(method, url, params):
    app_key = params.get("_key")
    if not app_key:
        webapp2.abort(400, "_key and _signature must be provided")

    signature = params.pop("_signature")
    if not signature:
        webapp2.abort(400, "_key and _signature must be provided")

    app_secret = key_store[app_key]
    params = urllib.urlencode(params)

    hashed = hmac.new(app_secret, "&".join((method.upper(), url, params)),
            hashlib.sha256)
    my_signature = binascii.b2a_base64(hashed.digest())

    return my_signature == signature    return my_signature == signature

