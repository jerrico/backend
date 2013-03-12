
from google.appengine.ext.ndb import Key
from google.appengine.api import users, urlfetch
from jerry.app_engine import Provider

from models import LogEntry

import hmac
import hashlib
import binascii
import webapp2
import json
import urllib
import config


class MySelfProvider(Provider):

    def __init__(self, *args, **kwargs):
        Provider.__init__(self, *args, **kwargs)
        self.app_access = Key(urlsafe=self.key).get()

    def _set_memcache(self, *args, **kwargs):
        # ignore internal memcache
        pass

    def _signin(self, user):
        state = self.app_access.compile_profile_state(user.user_id, user.device_id)
        user.load_state(state)

    def did(self, user, action, change, **kwargs):
        LogEntry.make(self.app_access.key, user.user_id, user.device_id,
            action=action, quantity=change, **kwargs).put()


def _get_jerry_provider():
    return MySelfProvider(**config.jerry)


def _get_user():
    user = users.get_current_user()
    if not user:
        webapp2.abort(400, "User needs to be logged in")

    user.jerry_profile = _get_jerry_provider().signin(user.user_id())
    return user


def verify_user(func):
    def wrapped(self, *args, **kwargs):
        self.user = _get_user()
        self.jerry_profile = self.user.jerry_profile
        return func(self, *args, **kwargs)
    return wrapped


def json_load_params(request):
    params = request.POST
    if not params:
        params = json.loads(request.body)
    return params


def understand_post(func):
    def wrapped(self, *args, **kwargs):
        return func(self, json_load_params(self.request), *args, **kwargs)
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

    app_access.jerry_profile = _get_jerry_provider().signin(app_access.owner.user_id())

    return app_access


def as_json(fun):
    def wrapped(handler, *args, **kwargs):
        wrap_it = not handler.request.params.get("_raw")
        debug = not handler.request.params.get("_debug")
        try:
            res = fun(handler, *args, **kwargs)
            if isinstance(res, webapp2.Response):
                # someone with a higher power knows what he is doing
                return res
            if wrap_it:
                res = {"status": "success", "result": res}
            handler.response.content_type = "application/json"
            handler.response.write(json.dumps(res))
        except webapp2.HTTPException, exc:
            if debug:
                raise
            handler.response.status = exc.code
            handler.response.content_type = "application/json"
            handler.response.write(json.dumps({
                "status": "error",
                "message": "{}".format(exc.message)
            }))
        except Exception, exc:
            if debug:
                raise
            handler.response.status = 500
            handler.response.content_type = "application/json"
            handler.response.write(json.dumps({
                "status": "error",
                "message": "{}".format(exc.message)
            }))
    return wrapped


def verified_api_request(func, without_key=False):
    def wrapped(handler, *args, **kwargs):
        params = dict(handler.request.params)
        if '_signature' in params:
            handler.app_access = verify_request(handler.request.method,
                    handler.request.path_url, params)
            handler.jerry_profile = handler.app_access.jerry_profile
        else:
            handler.user = _get_user()
            handler.jerry_profile = handler.user.jerry_profile
            if not without_key:
                handler.app_access = _get_key(params)

        return func(handler, *args, **kwargs)
    return as_json(wrapped)


def init_jerry_db():
    from google.appengine.ext.ndb import Key
    from models import AppAccess, Profile

    app = AppAccess(key=Key(urlsafe="agxkZXZ-ai1lcnJpY29yEAsSCUFwcEFjY2VzcxjpBww"),
            name="jerrico", secret="982b3800288b452a888e3bd31d982adf")

    app.put()

    Profile(name="free", default=True, parent=app.key).put()
    Profile(name="premium", default=False, parent=app.key).put()
    Profile(name="megalon", allow_per_default=True, parent=app.key).put()
