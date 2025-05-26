import pytest
import tkinter as tk
from a3 import LoginDialog, MainApp
from ds_messenger import DirectMessenger

def test_a3testrun():
    class DummyDialog:
        def __init__(self, *args, **kwargs):
            self.server = "127.0.0.1"
            self.username = "alice"
            self.password = "pass"

    @pytest.fixture(autouse=True)
    def patch_login(monkeypatch):
        monkeypatch.setattr("a3.LoginDialog", lambda root, title=None: DummyDialog())

    @pytest.mark.parametrize("auth_ok,offline,exit_code", [
        (True, False, 0),     # normal online
        (False, True, 0),     # offline fallback
        (False, False, 1),    # bad creds
    ])
    def test_main_flow(monkeypatch, tmp_path, capsys, auth_ok, offline, exit_code):
        class DM:
            def __init__(self, **kw): pass
            def authenticate(self):
                if offline:
                    raise ConnectionRefusedError()
                return auth_ok

        monkeypatch.setattr("a3.DirectMessenger", DM)
        #will add
        if offline:
            pass

        code = main()
        assert code == exit_code

