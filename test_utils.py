
from utils import verify_request
from webob import MultiDict

import webapp2
import cgi
import unittest
import hashlib
import binascii
import urllib
import hmac
import ndb_tests

from google.appengine.ext.ndb import model


class TestVerifier(ndb_tests.NDBTest):

    def setUp(self):
        super(TestVerifier, self).setUp()

        class AppAccess(model.Model):
            secret = model.StringProperty(required=True)

        self.eins_zwo = AppAccess(secret="meine weihnacht").put()
        self.other_key = AppAccess(secret="secret souce").put()

    def test_no_key(self):
        self.assertRaises(webapp2.HTTPException,
                verify_request, "GET", "http://example.com", {})

    def test_no_signature(self):
        self.assertRaises(webapp2.HTTPException,
                verify_request, "GET", "http://example.com", {"_key": ""})

    def test_unknown_key(self):
        self.assertRaises(webapp2.HTTPException,
                verify_request, "GET", "http://example.com",
                {"_key": self.other_key.urlsafe()[:4] + "blaa",
                        "_signature": "faulty"})

    def test_faulty_signature(self):
        self.assertFalse(verify_request("GET", "http://example.com",
                {"_key": self.eins_zwo.urlsafe(), "_signature": "faulty"}))

    def test_simple(self):
        key = self.eins_zwo.urlsafe()
        secret = "meine weihnacht"
        params = {"yay": "other", "second": "yes", "_key": key}
        query = '&'.join(("GET", "http://www.example.com",
                    urllib.urlencode(params)))
        params["_signature"] = binascii.b2a_base64(
            hmac.new(secret, query, hashlib.sha256).digest())

        self.assertTrue(verify_request("GET", "http://www.example.com",
                params))

    def test_lists(self):
        key = self.eins_zwo.urlsafe()
        secret = "meine weihnacht"
        params = {"yay": ["other", "peter", "michael"],
                "second": "yes", "_key": key}
        query = '&'.join(("GET", "http://www.example.com",
                    urllib.urlencode(params)))
        params["_signature"] = binascii.b2a_base64(
            hmac.new(secret, query, hashlib.sha256).digest())

        self.assertTrue(verify_request("GET", "http://www.example.com",
                params))

    def test_unsorted_params(self):
        key = self.eins_zwo.urlsafe()
        secret = "meine weihnacht"
        done_params = "c=b&a=b&_key=" + key
        query = '&'.join(("GET", "http://www.example.com",
                    done_params))
        params = MultiDict(cgi.parse_qsl(
                done_params, keep_blank_values=True,
                strict_parsing=False))
        params["_signature"] = binascii.b2a_base64(
            hmac.new(secret, query, hashlib.sha256).digest())

        self.assertTrue(verify_request("GET", "http://www.example.com",
                params))

    def test_post(self):
        key = self.other_key.urlsafe()
        secret = "secret souce"
        params = {"yay": "other", "second": "yes", "_key": key}
        query = '&'.join(("POST", "http://www.example.com",
                    urllib.urlencode(params)))
        params["_signature"] = binascii.b2a_base64(
            hmac.new(secret, query, hashlib.sha256).digest())

        self.assertTrue(verify_request("POST", "http://www.example.com",
                    params))

    def test_changed_params(self):
        key = self.eins_zwo.urlsafe()
        secret = "meine weihnacht"
        params = {"yay": "other", "second": "yes", "_key": key}
        query = '&'.join(("GET", "http://www.example.com",
                    urllib.urlencode(params)))
        params["_signature"] = binascii.b2a_base64(
            hmac.new(secret, query, hashlib.sha256).digest())

        # let's play with the params
        params["yay"] = "oupsi"

        self.assertFalse(verify_request("GET", "http://www.example.com",
                params))


if __name__ == "__main__":
    unittest.main()