
import urllib
import urllib2
import hashlib
import hmac
import binascii

key = "meinzwo"
secret = "herforder weihnacht"
params = {"yay": "other", "second": "yes"}
URL = "http://localhost:9092/?"


def run():
    params.update({
            "_key": key
        })
    query = urllib.urlencode(params)
    sha = hashlib.sha256()
    sha.update(secret + query)
    params["_signature"] = binascii.b2a_base64(
            hmac.new(secret, query, hashlib.sha256).digest())
    print URL, urllib.urlencode(params)
    req = urllib2.urlopen(URL + urllib.urlencode(params))
    import pdb
    pdb.set_trace()
    print req.read()

if __name__ == "__main__":
    run()
