#!/usr/bin/env python

from utils import verified_api_request, as_json
from google.appengine.ext import ndb
from models import LogEntry, AppAccess

import webapp2
import json


def verify_user(func):
    def wrapped(self, *args, **kwargs):
        from google.appengine.api import users

        user = users.get_current_user()
        if not user:
            webapp2.abort(400, "User needs to be logged in")
        self.user = user
        return func(self, *args, **kwargs)
    return wrapped


class Logger(webapp2.RequestHandler):

    @verified_api_request
    def get(self):
        query = LogEntry.query(ancestor=self.app_access.key
                    ).order(-LogEntry.when)
        return [x.prepare_json() for x in query.fetch(100)]

    @verified_api_request
    def post(self):
        device_id = self.request.POST.get("device_id")
        user_id = self.request.POST.get("user_id")
        if not device_id and not user_id:
            webapp2.abort(400, "either device_id or user_id must be provided")

        entries = json.loads(self.request.POST.get("entries"))
        app_key = self.app_access.key

        if isinstance(entries, dict):
            entries = [entries]

        keys = ndb.put_multi([LogEntry.make(app_key, user_id, device_id, **x)
                for x in entries])
        self.response.status = 201
        return {"entries": len(keys)}


class GetApps(webapp2.RequestHandler):

    @verify_user
    @as_json
    def get(self):
        return [x.prepare_json() for x in AppAccess.query()]


class VerifyAccess(webapp2.RequestHandler):

    @verified_api_request
    def get(self):
        return {"access": "granted"}

    @verified_api_request
    def post(self):
        return {"access": "granted"}

app = webapp2.WSGIApplication([
    ('/api/v1/verify_access', VerifyAccess),
    ('/api/v1/logger', Logger),
    ('/api/v0/my_apps', GetApps)
], debug=True)
