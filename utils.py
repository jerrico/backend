
from google.appengine.ext.ndb import Key

import hmac
import hashlib
import binascii
import webapp2
import json
import urllib


def verify_request(method, url, params):
    app_key = params.get("_key")
    if not app_key:
        webapp2.abort(400, "_key and _signature must be provided")

    signature = params.pop("_signature")
    if not signature:
        webapp2.abort(400, "_key and _signature must be provided")

    try:
        app_access = Key(urlsafe=app_key).get()
        app_secret = app_access.secret
    except Exception:
        webapp2.abort(401, "Unknown key: {}".format(app_key))

    params = urllib.urlencode(params)

    hashed = hmac.new(app_secret.encode("utf-8"),
            "&".join((method.upper(), url, params)), hashlib.sha256)
    my_signature = binascii.b2a_base64(hashed.digest())

    if my_signature != signature:
        webapp2.abort(403)

    return app_access


def as_json(fun):
    def wrapped(handler, *args, **kwargs):
        handler.response.content_type = "application/json"
        try:
            handler.response.write(json.dumps({
                    "status": "success",
                    "result": fun(handler, *args, **kwargs)
                    }))
        except webapp2.HTTPException, exc:
            handler.response.status = exc.code
            handler.response.write(json.dumps({
                "status": "error",
                "message": "{}".format(exc.message)
            }))
        except Exception, exc:
            handler.response.status = 500
            handler.response.write(json.dumps({
                "status": "error",
                "message": "{}".format(exc.message)
            }))
    return wrapped


def verified_api_request(func):
    def wrapped(handler, *args, **kwargs):
        handler.app_access = verify_request(handler.request.method,
                    handler.request.path_url,
                    handler.request.params)
        return func(handler, *args, **kwargs)
    return as_json(wrapped)
