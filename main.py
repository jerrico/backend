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
import webapp2
from utils import verify_request


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
        if not verify_request(handler.request.method, handler.request.params):
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
