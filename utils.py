
import hmac
import hashlib
import binascii
import webapp2
import json
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

    return my_signature == signature


def as_json(fun):
    def wrapped(handler, *args, **kwargs):
        handler.response.content_type = "application/json"
        try:
            handler.response.write(json.dumps(
                    fun(handler, *args, **kwargs)))
        except webapp2.HTTPException:
            raise
        except Exception, exc:
            handler.response.status = 500
            handler.response.write(json.dumps({
                "error": "{}".format(exc.__class__),
                "message": "{}".format(exc.message)
            }))
    return wrapped


def verified_api_request(func):
    def wrapped(handler, *args, **kwargs):
        if not verify_request(handler.request.method,
                    handler.request.path_url,
                    handler.request.params):
            webapp2.abort(403)

        return func(handler, *args, **kwargs)
    return as_json(wrapped)
