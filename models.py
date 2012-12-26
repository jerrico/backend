from google.appengine.ext import ndb


def date_json_format(dtm):
    return dtm.ctime()


class AppAccess(ndb.Model):
    name = ndb.StringProperty()
    active = ndb.BooleanProperty(default=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    secret = ndb.StringProperty(required=True, indexed=False)
    domain = ndb.StringProperty(indexed=False)

    def compile_profile_state(self, user_id=None, device_id=None):
        assert user_id or device_id, "user_id or device_id need to be specified"
        profile_key = None
        if user_id:
            user = ndb.Key(User, user_id, parent=self.key).get()
            if user:
                profile_key = user.assigned_profile
        if not profile_key and device_id:
            device = ndb.Key(Device, device_id, parent=self.key).get()
            if device:
                profile_key = device.assigned_profile
        if not profile_key:
            # find the fallback
            profile = Profile.query(ancestor=self.key, default=True).get()
            if not profile:
                raise ValueError()  # FIXME: we do not have any default here

            if user_id:
                User(id=user_id, parent=self.key,
                        assigned_profile=profile.key).put()
            if device_id:
                Device(id=device_id, parent=self.key,
                        assigned_profile=profile.key).put()
        else:
            profile = profile_key.get()

        states = {}
        for res in profile.restrictions:
            dictified = {"max": res.limit_to,
                    "left": res.limit_to,
                    "during": res.duration}
            try:
                states[res.action].append(dictified)
            except KeyError:
                states[res.action] = [dictified]

        return {
            "profile": profile.name,
            "default": profile.allow_per_default and "allow" or "deny",
            "states": states
            }


class Restriction(ndb.Model):
    # this is not a real model as it is a Structured on Profile
    action = ndb.StringProperty('a', required=True)
    limit_to = ndb.IntegerProperty('l', required=False)
    duration = ndb.StringProperty('d', required=False)


class Profile(ndb.Model):
    # key = parent => AppAccess
    name = ndb.StringProperty('n', required=True)
    created = ndb.DateTimeProperty('c', auto_now_add=True)
    last_change = ndb.DateTimeProperty('l', auto_now=True)
    default = ndb.BooleanProperty('d', default=False)
    allow_per_default = ndb.BooleanProperty('a', default=False)
    # following the restrictions
    restrictions = ndb.StructuredProperty(Restriction, repeated=True)


# for User Info
class User(ndb.Expando):
    # key = parent=>AppAccess; ID given by app
    assigned_profile = ndb.KeyProperty('p', kind=Profile, required=False)


# for Device Info
class Device(ndb.Expando):
    # key = parent=>AppAccess; Device-ID given
    assigned_profile = ndb.KeyProperty('p', kind=Profile, required=False)


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
