#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import hashlib
import urllib
import webapp2
import hmac
import binascii

key_store = {
    "test_app": "hidden_key",
    "meinzwo": "herforder weihnacht"
}


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
        params = handler.request.POST or handler.request.GET
        app_key = params.get("_key")
        signature = params.pop("_signature")
        if not app_key or not signature:
            webapp2.abort(400, "_key and _signature must be provided")
        app_secret = key_store[app_key]
        params = urllib.urlencode(params)

        hashed = hmac.new(app_secret, params, hashlib.sha256)
        my_signature = binascii.b2a_base64(hashed.digest())
        if my_signature != signature:
            webapp2.abort(403)

        return func(handler, *args, **kwargs)
    return as_json(wrapped)


class MainHandler(webapp2.RequestHandler):

    @verified_api_request
    def get(self):
        return {"yay": "me"}

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
