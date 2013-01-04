#!/usr/bin/env python

from utils import verified_api_request, as_json, understand_post, verify_user
from google.appengine.ext import ndb
from models import LogEntry, AppAccess, User, Device, Profile

import webapp2
import json


class ModelRestApi(webapp2.RequestHandler):
    model_cls = None
    no_item_raise = False
    writeable = ()

    @verified_api_request
    def get(self, item_id=None):
        # list service
        if not item_id:
            return [x.prepare_json() for x in self._get_query().fetch(100)]

        # specific item requested
        item = self._get_item_key(item_id).get()
        item_data = {}
        if item:
            item_data = item.prepare_json()
        elif self.no_item_raise:
            webapp2.abort(404, "Item not found")
        return item_data

    @verified_api_request
    @understand_post
    def post(self, params, item_id=None):
        if item_id:
            model = self._get_item_key(item_id).get()
            if model:
                return self._update_item(model, params)
            elif self.no_item_raise:
                webapp2.abort(404, "Item not found")
        return self._add_item(params)

    def _update_item(self, model, params):
        model.populate(**self._decorate_params(params))
        model.put()
        return model.prepare_json()

    def _add_item(self, params):
        model = self.model_cls(parent=self.app_access.key, **params)
        model.put()
        return model.prepare_json()

    def _get_item_key(self, item_id):
        return ndb.Key(self.model_cls, self._decorate_item_id(item_id),
                parent=self.app_access.key)

    def _get_query(self):
        return self._decorate_query(self.model_cls.query(
                    ancestor=self.app_access.key))

    def _decoreate_item_id(self, item_id):
        return item_id

    def _decorate_query(self, query):
        return query

    def _decorate_params(self, params):
        res_params = {}
        for key in self.writeable:
            if key in params:
                res_params[key] = params[key]
        return res_params


class Logger(ModelRestApi):

    model_cls = LogEntry

    def _decorate_query(self, query):
        return query.order(-LogEntry.when)

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


class Devices(ModelRestApi):
    model_cls = Device


class Users(ModelRestApi):
    model_cls = User


class Profiles(ModelRestApi):
    model_cls = Profile
    no_item_raise = True
    writeable = ('name', 'default', 'allow_per_default', "restrictions")

    def _add_item(self, params):
        name = params.get("name")
        if not name:
            webapp2.abort(400, "Please specify the name of the profile")
        model = self.model_cls(parent=self.app_access.key, name=name)
        model.put()
        return model.prepare_json()

    def _decorate_item_id(self, item_id):
        return int(item_id)


class AppsManager(webapp2.RequestHandler):

    def get(self):
        return [x.prepare_json() for x in AppAccess.query()]

    get = verified_api_request(get, without_key=True)

    @understand_post
    def post(self, params):
        name = params.get("name", None)
        if not name:
            webapp2.abort(400, "No app name given")
        app = AppAccess.create(name)
        app.put()
        return app.prepare_json()

    post = verified_api_request(post, without_key=True)


class VerifyAccess(webapp2.RequestHandler):

    @verified_api_request
    def get(self):
        return {"access": "granted"}

    @verified_api_request
    def post(self):
        return {"access": "granted"}

app = webapp2.WSGIApplication([
    ('/api/v1/verify_access', VerifyAccess),
    ('/api/v1/logs', Logger),
    ('/api/v1/profiles/(\d*?)', Profiles),
    ('/api/v1/profiles', Profiles),
    ('/api/v1/users/(.*?)', Users),
    ('/api/v1/users', Users),
    ('/api/v1/devices/(.*?)', Devices),
    ('/api/v1/devices', Devices),
    ('/api/v1/my_apps', AppsManager)
], debug=True)
