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
    monkeypatch.setenv("HOME", str(tmp_path))
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
                "timestamp": "123"}]}}

    notebook.save_user_data("me", data_in)

    out_file = redirect_store / "me.json"
    assert out_file.exists()

    data_out = notebook.load_user_data("me")
    assert data_out == data_in

def test_bad_json_fallback(redirect_store):

    notebook.save_user_data("alice", {"contacts": [], "messages": {}})
    json_path = redirect_store / "alice.json"

    json_path.write_text("{ not valid json }", encoding="utf-8")

    data = notebook.load_user_data("alice")
    assert data == {"contacts": [], "messages": {}}

def test_load_missing_file(redirect_store):

    data = notebook.load_user_data("nobody")
    assert data == {"contacts": [], "messages": {}}

def test_partial_data(redirect_store):

    redirect_store.mkdir(parents=True, exist_ok = True)
    f = redirect_store / "tom.json"
    f.write_text(json.dumps({"contacts": ["alice"]}), encoding="utf-8")
    data = notebook.load_user_data("tom")

    assert data == {"contacts": ["alice"]}


    f.write_text(json.dumps({"messages": {"bob": []}}), encoding="utf-8")
    data2 = notebook.load_user_data("tom")
    assert data2 == {"messages": {"bob": []}}

def test_overwrite(redirect_store):
    notebook.save_user_data("bob", {"contacts":["x"],"messages":{}})
    notebook.save_user_data("bob", {"contacts":["y"],"messages":{}})
    data = notebook.load_user_data("bob")
    assert data["contacts"] == ["y"]

def test_complex_structure(redirect_store):
    payload = {"contacts":["c1"], "messages":{"c1":[{"foo":"bar"}]}}
    notebook.save_user_data("x", payload)
    assert notebook.load_user_data("x") == payload