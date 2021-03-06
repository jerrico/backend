from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from datetime import datetime, timedelta
from uuid import uuid4


def date_json_format(dtm):
    return dtm.ctime()


class SetupIncomplete(Exception):
    pass


class NoDefaultDefined(SetupIncomplete):
    pass


class AppAccess(ndb.Model):
    name = ndb.StringProperty()
    active = ndb.BooleanProperty(default=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    secret = ndb.StringProperty(required=True, indexed=False)
    domain = ndb.StringProperty(indexed=False)
    payment_provider = ndb.StringProperty('p', choices=['', 'paymentwall'], default='')
    owner = ndb.UserProperty()

    @classmethod
    def create(cls, app_name, **kwargs):
        return cls(name=app_name, active=True, secret=uuid4().get_hex(), **kwargs)

    def prepare_json(self):
        prepped = self.to_dict()
        prepped["key"] = self.key.urlsafe()
        prepped["created"] = date_json_format(prepped["created"])
        prepped.pop("owner")
        return prepped

    def compile_profile_state(self, user_id=None, device_id=None, jerry_profile=None):
        assert user_id or device_id, "user_id or device_id need to be specified"
        profile_key = None
        user_key = None
        device_key = None
        user = None
        device = None
        if user_id:
            user_key = ndb.Key(User, user_id, parent=self.key)
            user = user_key.get()
            if user:
                profile_key = user.assigned_profile
        if not profile_key and device_id:
            device_key = ndb.Key(Device, device_id, parent=self.key)
            device = device_key.get()
            if device:
                profile_key = device.assigned_profile
        if not profile_key:
            # find the fallback
            profile = Profile.query(Profile.default == True, ancestor=self.key).get()
            if not profile:
                raise NoDefaultDefined()  # FIXME: we do not have any default here

            if user_id:
                user = User(id=user_id, parent=self.key,
                        account=profile.account, assigned_profile=profile.key)
                user.put()
                jerry_profile and jerry_profile.did("create_user")
            if device_id:
                device = Device(id=device_id, parent=self.key,
                        account=profile.account, assigned_profile=profile.key)
                device.put()
                jerry_profile and jerry_profile.did("create_device")
        else:
            profile = profile_key.get()

        query = LogEntry.query()
        if user_key:
            query = query.filter(LogEntry.user == user_key)
        elif device_key:
            query = query.filter(LogEntry.device == device_key)

        states = {}
        for res in profile.restrictions:
            try:
                states[res.action].append(res.compile_limitation(query))
            except KeyError:
                states[res.action] = [res.compile_limitation(query)]

        jerry_profile and jerry_profile.did("query_user")
        return {
            "profile": profile.name,
            "default": profile.allow_per_default and "allow" or "deny",
            "states": states,
            "account": user and user.prepare_json() or device.prepare_json()
            }


class Restriction(polymodel.PolyModel):
    # this is not a real model as it is a Structured on Profile
    action = ndb.StringProperty('a', required=True)

    def prepare_json(self):
        params = polymodel.PolyModel.to_dict(self)
        params["class_"] = params["class_"][-1]
        return params

    def compile_limitation(self, query):
        return self.prepare_json()


class BinaryRestriction(Restriction):
    allow = ndb.BooleanProperty('b', default=False)


class PerTimeRestriction(Restriction):
    limit_to = ndb.IntegerProperty('l', required=True)
    duration = ndb.IntegerProperty('d', required=True)

    def compile_limitation(self, query):
        limitation = Restriction.compile_limitation(self, query)
        query = query.filter(LogEntry.action == self.action,
                    LogEntry.when > (datetime.now() - timedelta(seconds=self.duration)))
        limitation["left"] = self.limit_to - query.count()
        return limitation


class TotalAmountRestriction(Restriction):
    total_max = ndb.IntegerProperty('m', required=True)

    def compile_limitation(self, query):
        limitation = Restriction.compile_limitation(self, query)
        query = query.filter(LogEntry.action == self.action)
        limitation["left"] = self.total_max - query.count()
        return limitation


class LocalAmountRestriction(Restriction):
    local_max = ndb.IntegerProperty('m', required=True)


class AccountAmountRestriction(Restriction):
    account_item = ndb.StringProperty('i', required=True)
    quantity_change = ndb.IntegerProperty('q', required=False, default=1)

RestrictionTypes = {
    "BinaryRestriction": BinaryRestriction,
    "PerTimeRestriction": PerTimeRestriction,
    "TotalAmountRestriction": TotalAmountRestriction,
    "LocalAmountRestriction": LocalAmountRestriction,
    "AccountAmountRestriction": AccountAmountRestriction,
}

class AccountData(ndb.Expando):
    pass


class Profile(ndb.Model):
    # key = parent => AppAccess
    name = ndb.StringProperty('n', required=True)
    created = ndb.DateTimeProperty('c', auto_now_add=True)
    last_change = ndb.DateTimeProperty('l', auto_now=True)
    default = ndb.BooleanProperty('d', default=False)
    allow_per_default = ndb.BooleanProperty('a', default=False)
    account = ndb.StructuredProperty(AccountData, 'ad')
    payment_id = ndb.StringProperty('p')
    # following the restrictions
    restrictions = ndb.LocalStructuredProperty(Restriction, compressed=True,
                repeated=True)

    def prepare_json(self, short=False):
        prepped = self.to_dict()
        prepped["id"] = self.key.id()
        prepped["created"] = date_json_format(prepped["created"])
        prepped["last_change"] = date_json_format(prepped["last_change"])
        if short:
            for x in ("restrictions", "account", 'payment_id'):
                prepped.pop(x)
        else:
            prepped["restrictions"] = [x.prepare_json() for x in self.restrictions]
            prepped['account'] = self.account and self.account.to_dict() or dict()
        return prepped

    def _pre_put_hook(self):
        if self.default:
            cur_default = Profile.query(Profile.default == True,
                        ancestor=self.key.parent()).get()
            if cur_default and cur_default != self:
                cur_default.default = False
                cur_default.put()


class UDHelper:

    def prepare_json(self):
        resp = {'account': self.account and self.account.to_dict() or dict()}
        resp["assigned_profile"] = self.assigned_profile.get().prepare_json(short=True)
        resp['id'] = self.key.id()
        resp['uuid'] = self.key.urlsafe()
        return resp


# for User Info
class User(UDHelper, ndb.Model):
    # key = parent=>AppAccess; ID given by app
    assigned_profile = ndb.KeyProperty('p', kind=Profile, required=False)
    account = ndb.StructuredProperty(AccountData, 'a')

    def make_log(self, action, **kwargs):
        return LogEntry.make(self.key.parent(), self.key.id(), None, action=action, **kwargs)


# for Device Info
class Device(UDHelper, ndb.Model):
    # key = parent=>AppAccess; Device-ID given
    assigned_profile = ndb.KeyProperty('p', kind=Profile, required=False)
    account = ndb.StructuredProperty(AccountData, 'a')

    def make_log(self, action, **kwargs):
        return LogEntry.make(self.key.parent(), None, self.key.id(), action=action, **kwargs)


class Transaction(ndb.Model):
    when = ndb.DateTimeProperty('w', auto_now_add=True)
    changed = ndb.DateTimeProperty('c', auto_now=True)
    target = ndb.KeyProperty('t')
    state = ndb.StringProperty('s', choices=['open', 'cancelled', 'accomplished'], default="open")


class LogEntry(ndb.Expando):
    # key = parent=>AppAccess
    when = ndb.DateTimeProperty("w", auto_now_add=True)
    user = ndb.KeyProperty("us", kind=User, required=False)
    device = ndb.KeyProperty("d", kind=Device, required=False)
    action = ndb.StringProperty("a", required=True, indexed=True)
    quantity = ndb.IntegerProperty("q", required=False, indexed=False, default=1)
    unit = ndb.StringProperty("un", required=False, indexed=False)

    def prepare_json(self):
        prepped = {}
        for key, val in self.to_dict().iteritems():
            if isinstance(val, ndb.Key):
                val = val.id()
            prepped[key] = val
        prepped["id"] = self.key.id()
        prepped["when"] = date_json_format(prepped["when"])
        prepped["user"] = self.user and self.user.id()
        prepped["device"] = self.device and self.device.id()
        return prepped

    @classmethod
    def make(cls, app_key, user_id, device_id, **params):
        if user_id:
            params["user"] = ndb.Key(User, user_id, parent=app_key)
        if device_id:
            params["device"] = ndb.Key(Device, device_id, parent=app_key)
        params["parent"] = app_key
        return cls(**params)
