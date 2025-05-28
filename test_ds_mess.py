import io
import socket
import pytest
import time
from ds_messenger import DirectMessenger, DirectMessage

def test_alicebob():
    alice = DirectMessenger(username='alice', password='password')
    bob   = DirectMessenger(username='bob',   password='password')

    assert alice.authenticate(), "Alice login failed"
    assert bob.authenticate(),   "Bob login failed"

    ok = alice.send_msg("Hello Bob!", "bob")
    print("Alice→Bob send OK:", ok)

    time.sleep(0.1)

    new = bob.retrieve_new()
    print("Bob got messages:", [(dm.sender, dm.message) for dm in new])

    all_msgs = alice.retrieve_all()
    print("Alice conversation:", [(dm.sender or alice.username, dm.message) for dm in all_msgs])

class DummySocket:
    def __init__(self, responses):
        self._rbuf = io.StringIO("\n".join(responses) + "\n")
        self._wbuf = io.StringIO()

    def makefile(self, mode):
        return self._rbuf if "r" in mode else self._wbuf

def patch_socket(monkeypatch, responses):
    dummy = DummySocket(responses)
    monkeypatch.setattr(socket, "create_connection", lambda addr: dummy)
    return dummy

def test_authenticate_success(monkeypatch):
    dummy = patch_socket(monkeypatch, ['{"response":{"type":"ok","message":"W","token":"TK"}}'])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate() is True
    assert dm.token == "TK"

def test_authenticate_error(monkeypatch):
    dummy = patch_socket(monkeypatch, ['{"response":{"type":"error","message":"wrong"}}'])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate() is False
    assert dm.token is None

def test_send_msg_and_retrieve(monkeypatch):
    dummy = patch_socket(monkeypatch, [
        '{"response":{"type":"ok","message":"W","token":"TK2"}}',
        '{"response":{"type":"ok","message":"sent"}}',
        '{"response":{"type":"ok","messages":[{"message":"hey","from":"alice","timestamp":"1"}]}}', ])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate() is True

    sent_ok = dm.send_msg("yo", "bob")
    assert sent_ok is True

    new = dm.retrieve_new()
    assert len(new) == 1
    msg = new[0]
    assert isinstance(msg, DirectMessage)
    assert msg.sender == "alice"
    assert msg.message == "hey"

def test_retrieve_all(monkeypatch):
    dummy = patch_socket(monkeypatch, [
        '{"response":{"type":"ok","message":"W","token":"TK3"}}',
        '{"response":{"type":"ok","messages":[{"message":"hi","from":"bob","timestamp":"2"},{"message":"yo","recipient":"bob","timestamp":"3"}]}}'])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate() is True

    all_msgs = dm.retrieve_all()
    assert len(all_msgs) == 2

    assert any(m.sender == "bob" for m in all_msgs)
    assert any(m.recipient == "bob" for m in all_msgs)
##
def test_authenticate_with_args(monkeypatch):
    dummy = patch_socket(monkeypatch, [
        '{"response":{"type":"ok","message":"OK","token":"TOK"}}'])
    dm = DirectMessenger(host="h", port=1, username="orig", password="origpw")
    ok = dm.authenticate(username="newuser", password="newpw")
    assert ok is True
    assert dm.username == "newuser"
    assert dm.password == "newpw"
    assert dm.token == "TOK"

def test_send_msg_updates_local(monkeypatch):
    monkeypatch.setattr("ds_messenger.load_user_data", lambda u: {"contacts": [], "messages": {}})
    monkeypatch.setattr("ds_messenger.save_user_data", lambda u, d: None)

    dummy = patch_socket(monkeypatch, [
        '{"response":{"type":"ok","message":"Auth","token":"TKN"}}',
        '{"response":{"type":"ok","message":"Sent"}}'])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate()
    result = dm.send_msg("hello", "bob")
    assert result is True

    assert "bob" in dm._local["contacts"]
    assert dm._local["messages"]["bob"][-1]["message"] == "hello"

def test_retrieve_new_updates_local(monkeypatch):
    monkeypatch.setattr("ds_messenger.load_user_data", lambda u: {"contacts": [], "messages": {}})
    monkeypatch.setattr("ds_messenger.save_user_data", lambda u, d: None)

    dummy = patch_socket(monkeypatch, [
        '{"response":{"type":"ok","message":"Auth","token":"TKN"}}',
        '{"response":{"type":"ok","messages":[{"message":"hi","from":"alice","timestamp":"123"}]}}'])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate()
    new = dm.retrieve_new()
    assert len(new) == 1 and isinstance(new[0], DirectMessage)

    assert "alice" in dm._local["contacts"]
    assert "alice" in dm._local["messages"]



def test_send_msg_new_contact(monkeypatch):
    dummy = patch_socket(monkeypatch, [
        '{"response":{"type":"ok","message":"Welcome","token":"TK1"}}',
        '{"response":{"type":"ok","message":"Sent"}}'])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate() is True
    dm._local = {"contacts": [], "messages": {}}

    assert dm._local["contacts"] == []

    ok = dm.send_msg("hello bob", "bob")
    assert ok is True

    assert dm._local["contacts"] == ["bob"]
    msgs = dm._local["messages"]["bob"]
    assert msgs and msgs[-1]["message"] == "hello bob"


def test_send_msg_existing_contact(monkeypatch):
    dummy = patch_socket(monkeypatch, [
        '{"response":{"type":"ok","message":"Welcome","token":"TK2"}}',
        '{"response":{"type":"ok","message":"Sent"}}'])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate() is True
    dm._local = {"contacts": [], "messages": {}}

    dm._local = {"contacts": ["bob"], "messages": {"bob": []}}

    ok = dm.send_msg("second msg", "bob")
    assert ok is True

    assert dm._local["contacts"] == ["bob"]
    assert dm._local["messages"]["bob"][-1]["message"] == "second msg"


def test_send_msg_failure_leaves_local(monkeypatch):
    dummy = patch_socket(monkeypatch, [
        '{"response":{"type":"ok","message":"Welcome","token":"TK3"}}',
        '{"response":{"type":"error","message":"fail to send"}}'])

    dm = DirectMessenger(host="h", port=1, username="u", password="p")
    assert dm.authenticate() is True
    dm._local = {"contacts": [], "messages": {}}

    assert dm._local["contacts"] == []

    ok = dm.send_msg("won't arrive", "bob")
    assert ok is False

    assert dm._local["contacts"] == []
    assert dm._local["messages"] == {}