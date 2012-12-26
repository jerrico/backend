import unittest
import ndb_tests
from datetime import datetime, timedelta

from models import (LogEntry, AppAccess, User, Device,
        Profile, Restriction)


class SimpleProfilerTest(ndb_tests.NDBTest):

    def _load_simple(self):
        app = AppAccess(secret="test").put()
        free = Profile(parent=app, name="free", default=True,
            restrictions=[
                # unlimited:
                Restriction(action="take_photo"),
                # simple:
                Restriction(action="upload_photo",
                            limit_to=10, duration="a day"),
                # double restriction:
                Restriction(action="share_photo",
                            limit_to=10, duration="a day"),
                Restriction(action="share_photo",
                            limit_to=20, duration="a week"),
            ]).put()
        premium = Profile(parent=app, name="premium", allow_per_default=True,
            restrictions=[
                # simple:
                Restriction(action="upload_photo",
                            limit_to=100, duration="a day")
            ]).put()
        User(id="free_u", parent=app, assigned_profile=free).put()
        User(id="prem", parent=app, assigned_profile=premium).put()

        Device(id="AMEI_FREE", parent=app, assigned_profile=free).put()
        Device(id="MIAU_PREM", parent=app, assigned_profile=premium).put()

        self.app_access = app.get()

    def ResetKindMap(self):
        # we run on live models
        pass

    def test_simple(self):
        self._load_simple()
        profile_state = self.app_access.compile_profile_state(user_id="free_u")
        self.assertEquals(profile_state["profile"], "free")
        self.assertEquals(profile_state["default"], "deny")
        self.assertEquals(len(profile_state["states"]), 3)
        self.assertEquals(profile_state["states"]["take_photo"], [True])
        self.assertEquals(profile_state["states"]["share_photo"][0]["left"], 10)
        self.assertEquals(profile_state["states"]["share_photo"][0]["max"], 10)

    def test_with_simple_counter(self):
        self._load_simple()
        LogEntry.make(self.app_access.key, "free_u", None,
                    action="share_photo").put()

        profile_state = self.app_access.compile_profile_state(user_id="free_u")
        self.assertEquals(profile_state["profile"], "free")
        self.assertEquals(profile_state["default"], "deny")
        self.assertEquals(len(profile_state["states"]), 3)
        self.assertEquals(profile_state["states"]["share_photo"][0]["left"], 9)
        self.assertEquals(profile_state["states"]["share_photo"][0]["max"], 10)

        LogEntry.make(self.app_access.key, "free_u", None,
                    action="share_photo").put()

        profile_state = self.app_access.compile_profile_state(user_id="free_u")
        self.assertEquals(profile_state["profile"], "free")
        self.assertEquals(profile_state["default"], "deny")
        self.assertEquals(len(profile_state["states"]), 3)
        self.assertEquals(profile_state["states"]["share_photo"][0]["left"], 8)
        self.assertEquals(profile_state["states"]["share_photo"][0]["max"], 10)

    def test_with_outer_user_counter(self):
        self._load_simple()
        LogEntry.make(self.app_access.key, "free_u", None,
                    action="share_photo").put()
        # none user
        LogEntry.make(self.app_access.key, "other", None,
                    action="share_photo").put()

        profile_state = self.app_access.compile_profile_state(user_id="free_u")
        self.assertEquals(profile_state["profile"], "free")
        self.assertEquals(profile_state["default"], "deny")
        self.assertEquals(len(profile_state["states"]), 3)
        self.assertEquals(profile_state["states"]["share_photo"][0]["left"], 9)
        self.assertEquals(profile_state["states"]["share_photo"][0]["max"], 10)

    def test_with_yesterday_counter(self):
        self._load_simple()
        LogEntry.make(self.app_access.key, "free_u", None,
                    action="share_photo").put()
        # none user
        LogEntry.make(self.app_access.key, "free_u", None,
                    action="share_photo",
                    when=datetime.now() - timedelta(hours=25)).put()

        profile_state = self.app_access.compile_profile_state(user_id="free_u")
        self.assertEquals(profile_state["profile"], "free")
        self.assertEquals(profile_state["default"], "deny")
        self.assertEquals(len(profile_state["states"]), 3)
        self.assertEquals(profile_state["states"]["share_photo"][0]["left"], 9)
        self.assertEquals(profile_state["states"]["share_photo"][0]["max"], 10)



    def test_no_user_nor_device(self):
        self._load_simple()
        self.assertRaises(AssertionError,
                self.app_access.compile_profile_state)

    def test_user_hihgher_than_device(self):
        self._load_simple()
        profile_state = self.app_access.compile_profile_state(
                user_id="free_u", device_id="MIAU_PREM")
        self.assertEquals(profile_state["profile"], "free")
        self.assertEquals(profile_state["default"], "deny")
        self.assertEquals(len(profile_state["states"]), 3)

    def test_device_fallback(self):
        self._load_simple()
        profile_state = self.app_access.compile_profile_state(
                user_id="faulty_id", device_id="MIAU_PREM")
        self.assertEquals(profile_state["profile"], "premium")
        self.assertEquals(profile_state["default"], "allow")
        self.assertEquals(len(profile_state["states"]), 1)



if __name__ == "__main__":
    unittest.main()