import pytest
import a3

class DummyDialog:
    def __init__(self, root, title=None):
        self.server   = "127.0.0.1"
        self.username = "alice"
        self.password = "pass"

@pytest.fixture(autouse=True)
def stub_login(monkeypatch):
    monkeypatch.setattr(a3, "LoginDialog", DummyDialog)

@pytest.mark.parametrize("auth_ok, offline, expected", [
    (True,  False, 0),  # online ok
    (False, True,  0),  # offline fallback
    (False, False, 1),  # bad creds
])
def test_main_flow(monkeypatch, tmp_path, auth_ok, offline, expected):
    # 1) stub DirectMessenger
    class FakeDM:
        def __init__(self, *, host, port, username, password):
            self.username = username
        def authenticate(self):
            if offline:
                raise ConnectionRefusedError()
            return auth_ok
        def retrieve_new(self):
            return []
        def retrieve_all(self):
            return []

    monkeypatch.setattr(a3, "DirectMessenger", FakeDM)

    # 2) seed local data for offline fallback
    if offline and expected == 0:
        monkeypatch.setenv("HOME", str(tmp_path))
        from notebook import save_user_data
        save_user_data("alice", {"contacts":["bob"], "messages":{}})

    # 3) run main() — shouldn't raise now
    code = a3.main()
    assert code == expected
