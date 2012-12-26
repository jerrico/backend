import unittest
import ndb_tests

from models import (LogEntry, AppAccess, User, Device,
        Profile, Restriction)


class ProfilerTest(ndb_tests.NDBTest):

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

    def test_simple(self):
        self._load_simple()
        profile_state = self.app_access.compile_profile_state(user_id="free_u")
        self.assertEquals(profile_state["profile"], "free")

    def test_no_user_nor_device(self):
        self._load_simple()
        self.assertRaises(AssertionError,
                self.app_access.compile_profile_state)

    def test_user_hihgher_than_device(self):
        self._load_simple()
        profile_state = self.app_access.compile_profile_state(
                user_id="free_u", device_id="MIAU_PREM")
        self.assertEquals(profile_state["profile"], "free")

    def test_device_fallback(self):
        self._load_simple()
        profile_state = self.app_access.compile_profile_state(
                user_id="faulty_id", device_id="MIAU_PREM")
        self.assertEquals(profile_state["profile"], "premium")

    def ResetKindMap(self):
        # we run on live models
        pass


if __name__ == "__main__":
    unittest.main()