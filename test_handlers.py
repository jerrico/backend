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

from google.appengine.ext.ndb import model


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

        class AppAccess(model.Model):
            secret = model.StringProperty(required=True)

        self._default_access = AppAccess(secret="meine weihnacht").put()

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

    def setUp(self):
        super(VerifyAccessTest, self).setUp()

    def test_simple(self):
        self.get(a="b", c="d")

    def test_post(self):
        self.post(a="b", c="d")

if __name__ == "__main__":
    unittest.main()