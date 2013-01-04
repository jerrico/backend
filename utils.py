
from google.appengine.ext.ndb import Key
from google.appengine.api import users

import hmac
import hashlib
import binascii
import webapp2
import json
import urllib


def _get_user():
    user = users.get_current_user()
    if not user:
        webapp2.abort(400, "User needs to be logged in")
    return user


def verify_user(func):
    def wrapped(self, *args, **kwargs):
        self.user = _get_user()
        return func(self, *args, **kwargs)
    return wrapped


def understand_post(func):
    def wrapped(self, *args, **kwargs):
        params = self.request.POST
        if not params:
            params = json.loads(self.request.body)
        return func(self, params, *args, **kwargs)
    return wrapped


def _get_key(params):
    app_key = params.get("_key")
    if not app_key:
        webapp2.abort(400, "_key and _signature must be provided")
    try:
        app_access = Key(urlsafe=app_key).get()
        secret = app_access.secret
    except Exception:
        webapp2.abort(401, "Unknown key: {}".format(app_key))
    return app_access


def verify_request(method, url, params):
    signature = params.pop("_signature")
    if not signature:
        webapp2.abort(400, "_key and _signature must be provided")

    app_access = _get_key(params)
    app_secret = app_access.secret

    enc_params = urllib.urlencode(params)

    hashed = hmac.new(app_secret.encode("utf-8"),
            "&".join((method.upper(), url, enc_params)), hashlib.sha256)
    my_signature = binascii.b2a_base64(hashed.digest())

    if my_signature != signature:
        webapp2.abort(403, "invalid signature")

    return app_access


def as_json(fun):
    def wrapped(handler, *args, **kwargs):
        handler.response.content_type = "application/json"
        wrap_it = not handler.request.params.get("_raw")
        try:
            res = fun(handler, *args, **kwargs)
            if wrap_it:
                res = {"status": "success", "result": res}
            handler.response.write(json.dumps(res))
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


def verified_api_request(func, without_key=False):
    def wrapped(handler, *args, **kwargs):
        params = handler.request.method == "POST" and \
                handler.request.POST or handler.request.GET
        if '_signature' in params:
            handler.app_access = verify_request(handler.request.method,
                    handler.request.path_url, params)
        else:
            handler.user = _get_user()
            if not without_key:
                handler.app_access = _get_key(params)
        return func(handler, *args, **kwargs)
    return as_json(wrapped)
