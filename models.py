from google.appengine.ext import ndb


def date_json_format(dtm):
    return dtm.ctime()


class AppAccess(ndb.Model):
    name = ndb.StringProperty()
    active = ndb.BooleanProperty(default=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    secret = ndb.StringProperty(required=True, indexed=False)
    domain = ndb.StringProperty(indexed=False)


# for User Info
class User(ndb.Expando):
    # key = parent=>AppAccess; ID given to app
    pass


# for Device Info
class Device(ndb.Expando):
    # key = parent=>AppAccess; Device-ID given
    pass


class LogEntry(ndb.Model):
    # key = parent=>AppAccess
    when = ndb.DateTimeProperty("w", auto_now_add=True)
    user = ndb.KeyProperty("us", kind=User, required=False)
    device = ndb.KeyProperty("d", kind=Device, required=False)
    action = ndb.StringProperty("a", required=True, indexed=True)
    quantity = ndb.IntegerProperty("q", required=False, indexed=False, default=1)
    unit = ndb.StringProperty("un", required=False, indexed=False)

    def prepare_json(self):
        prepped = self.to_dict()
        prepped["when"] = date_json_format(prepped["when"])
        return prepped

    @classmethod
    def make(cls, app_key, user_id, device_id, **params):
        if user_id:
            params["user"] = ndb.Key(User, user_id, parent=app_key)
        if device_id:
            params["device"] = ndb.Key(Device, device_id, parent=app_key)
        params["parent"] = app_key
        return cls(**params)
