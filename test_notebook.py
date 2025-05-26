# test_notebook.py

import json
from pathlib import Path
import pytest
import notebook

@pytest.fixture(autouse=True)
def redirect_store(tmp_path, monkeypatch):
    """
    Every test: override notebook.STORE_DIR so
    that save/load happen under tmp_path / 'store'
    """
    fake = tmp_path / "store"
    monkeypatch.setenv("HOME", str(tmp_path))        # just in case
    monkeypatch.setattr(notebook, "STORE_DIR", fake)
    return fake

def test_roundtrip(redirect_store):
    data_in = {
        "contacts": ["bob"],
        "messages": {
            "bob": [{
                "sender":    "bob",
                "recipient": "me",
                "message":   "hi",
                "timestamp": "123"
            }]
        }
    }

    # 1) save
    notebook.save_user_data("me", data_in)

    # 2) file must exist under fake store
    out_file = redirect_store / "me.json"
    assert out_file.exists()

    # 3) load it back
    data_out = notebook.load_user_data("me")
    assert data_out == data_in

def test_bad_json_fallback(redirect_store):
    # create a valid file so the folder is there
    notebook.save_user_data("alice", {"contacts": [], "messages": {}})
    json_path = redirect_store / "alice.json"

    # stomp it with invalid JSON
    json_path.write_text("{ not valid json }", encoding="utf-8")

    # loader should *not* raise, but return the default
    data = notebook.load_user_data("alice")
    assert data == {"contacts": [], "messages": {}}
