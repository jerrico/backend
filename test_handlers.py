# -*- coding: utf-8 -*-
import main
import webapp2
import webtest
import unittest
import ndb_tests
import urllib
import binascii
import hmac
import hashlib
import json

from google.appengine.ext.ndb import model
from models import LogEntry, AppAccess


class HandlerMixin(object):
    handler_cls = None
    path = "/"

    def setUp(self):
        super(HandlerMixin, self).setUp()
        # Create a WSGI application.
        app = webapp2.WSGIApplication([(self.path, self.handler_cls)])
        # Wrap the app with WebTest’s TestApp.
        self.testapp = webtest.TestApp(app)


class ApiHandlerMixin(HandlerMixin):

    def _sign(self, method, url, params, key=None, secret=None):
        if not key:
            key = self._default_access.urlsafe()
        if not secret:
            secret = self._default_access.get().secret.encode("utf-8")
        params["_key"] = key
        encoded = urllib.urlencode(params)
        query = "&".join((method.upper(), url, encoded))
        encoded += "&_signature=" + urllib.quote(binascii.b2a_base64(
                hmac.new(secret, query, hashlib.sha256).digest()))
        return encoded

    def setUp(self):
        super(ApiHandlerMixin, self).setUp()
        self._default_access = AppAccess(secret="meine weihnacht").put()

    def ResetKindMap(self):
        # we run on live models
        pass

    def get(self, key=None, secret=None, **params):
        signed_url = self._sign("GET", "http://localhost" + self.path,
                    params, key, secret)
        return self.testapp.get(self.path, params=signed_url)

    def post(self, key=None, secret=None, **params):
        signed_url = self._sign("POST", "http://localhost" + self.path,
                    params, key, secret)
        return self.testapp.post(self.path, params=signed_url)


class VerifyAccessTest(ApiHandlerMixin, ndb_tests.NDBTest):

    handler_cls = main.VerifyAccess

    def test_simple(self):
        self.get(a="b", c="d")

    def test_post(self):
        self.post(a="b", c="d")


class LoggerTest(ApiHandlerMixin, ndb_tests.NDBTest):

    handler_cls = main.Logger

    def test_simple(self):
        self.post(device_id="AMEI", entries=json.dumps([
                {"action": "upload_photo"}]))
        self.assertEquals(LogEntry.query().count(), 1)
        entry = LogEntry.query().get()
        self.assertEquals(entry.action, "upload_photo")
        self.assertEquals(entry.quantity, 1)
        self.assertEquals(entry.device.string_id(), "AMEI")
        self.assertTrue(entry.user is None)
        self.assertEquals(entry.key.parent(), self._default_access)

    def test_none_list(self):
        self.post(device_id="AMEI", entries=json.dumps(
                {"action": "upload_photo"}))
        self.assertEquals(LogEntry.query().count(), 1)
        entry = LogEntry.query().get()
        self.assertEquals(entry.action, "upload_photo")
        self.assertEquals(entry.quantity, 1)
        self.assertEquals(entry.device.string_id(), "AMEI")
        self.assertTrue(entry.user is None)
        self.assertEquals(entry.key.parent(), self._default_access)

    def test_with_userd_list(self):
        self.post(user_id="custom_user_g+0001", entries=json.dumps(
                {"action": "start_app"}))
        self.assertEquals(LogEntry.query().count(), 1)
        entry = LogEntry.query().get()
        self.assertEquals(entry.action, "start_app")
        self.assertEquals(entry.quantity, 1)
        self.assertEquals(entry.user.string_id(), "custom_user_g+0001")
        self.assertTrue(entry.device is None)
        self.assertEquals(entry.key.parent(), self._default_access)

    def test_multiple(self):
        self.post(device_id="Meito", entries=json.dumps([
                {"action": "upload_photo"},
                {"action": "upload_photo"}
                ]))
        self.assertEquals(LogEntry.query().count(), 2)
        for entry in LogEntry.query():
            self.assertEquals(entry.quantity, 1)
            self.assertEquals(entry.device.string_id(), "Meito")
            self.assertTrue(entry.user is None)
            self.assertEquals(entry.key.parent(), self._default_access)

    def test_user_and_device(self):
        self.post(user_id="custom_user_g+0004", device_id="Ameito192",
                entries=json.dumps([{"action": "start_app"}]))
        self.assertEquals(LogEntry.query().count(), 1)
        entry = LogEntry.query().get()
        self.assertEquals(entry.action, "start_app")
        self.assertEquals(entry.quantity, 1)
        self.assertEquals(entry.user.string_id(), "custom_user_g+0004")
        self.assertEquals(entry.device.string_id(), "Ameito192")
        self.assertEquals(entry.key.parent(), self._default_access)

    def test_no_user_nor_device(self):
        self.post(entries=json.dumps([{"action": "start_app"}]))

if __name__ == "__main__":
    unittest.main()