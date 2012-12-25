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

import webapp2
from models import LogEntry
from utils import verified_api_request


class Logger(webapp2.RequestHandler):

    @verified_api_request
    def get(self):
        return []

    @verified_api_request
    def post(self):
        pass


class VerifyAccess(webapp2.RequestHandler):

    @verified_api_request
    def get(self):
        return {"access": "granted"}

app = webapp2.WSGIApplication([
    ('/api/v1/verify_access', VerifyAccess),
    ('/api/v1/logger', Logger)
], debug=True)
