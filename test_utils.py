
from utils import verify_request

import webapp2
import unittest
import hashlib
import binascii
import urllib
import hmac


class TestVerifier(unittest.TestCase):

    def test_no_key(self):
        self.assertRaises(webapp2.HTTPException,
                verify_request, "GET", "http://example.com", {})

    def test_no_signature(self):
        self.assertRaises(webapp2.HTTPException,
                verify_request, "GET", "http://example.com", {"_key": ""})

    def test_unknown_key(self):
        self.assertRaises(webapp2.HTTPException,
                verify_request, "GET", "http://example.com",
                {"_key": "blabla", "_signature": "faulty"})

    def test_faulty_signature(self):
        self.assertFalse(verify_request("GET", "http://example.com",
                {"_key": "meinzwo", "_signature": "faulty"}))

    def test_simple(self):
        key = "meinzwo"
        secret = "herforder weihnacht"
        params = {"yay": "other", "second": "yes", "_key": key}
        query = '&'.join(("GET", "http://www.example.com",
                    urllib.urlencode(params)))
        params["_signature"] = binascii.b2a_base64(
            hmac.new(secret, query, hashlib.sha256).digest())

        self.assertTrue(verify_request("GET", "http://www.example.com",
                params))

    def test_post(self):
        key = "meinzwo"
        secret = "herforder weihnacht"
        params = {"yay": "other", "second": "yes", "_key": key}
        query = '&'.join(("POST", "http://www.example.com",
                    urllib.urlencode(params)))
        params["_signature"] = binascii.b2a_base64(
            hmac.new(secret, query, hashlib.sha256).digest())

        self.assertTrue(verify_request("POST", "http://www.example.com",
                    params))

    def test_changed_params(self):
        key = "meinzwo"
        secret = "herforder weihnacht"
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