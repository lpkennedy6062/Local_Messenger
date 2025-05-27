import json
import pytest
from ds_protocol import (
    make_auth,
    make_directmessage,
    make_fetch,
    extract_json,
    ServerResponse,
)

def test_make_auth():
    j = make_auth("u", "p")
    obj = json.loads(j)
    assert "authenticate" in obj
    assert obj["authenticate"]["username"] == "u"
    assert obj["authenticate"]["password"] == "p"

def test_make_directmessage():
    j = make_directmessage("tok", "hi", "bob", "123.456")
    obj = json.loads(j)
    assert obj["token"] == "tok"
    dm = obj["directmessage"]
    assert dm["entry"] == "hi"
    assert dm["recipient"] == "bob"
    assert dm["timestamp"] == "123.456"

@pytest.mark.parametrize("what", ["all", "unread"])
def test_make_fetch(what):
    j = make_fetch("tok2", what)
    obj = json.loads(j)
    assert obj["token"] == "tok2"
    assert obj["fetch"] == what

def test_parse_ok_response():
    sample = '{"response": {"type":"ok", "message":"hello","token":"T"}}'
    r = extract_json(sample)
    assert isinstance(r, ServerResponse)
    assert r.type == "ok"
    assert r.message == "hello"
    assert r.token == "T"

def test_parse_error_response():
    sample = '{"response": {"type":"error", "message":"bad"}}'
    r = extract_json(sample)
    assert r.type == "error"
    assert r.message == "bad"
    assert r.token is None

def test_parse_malformed_raises():
    with pytest.raises(ValueError):
        extract_json("not a json")

def test_parse_missing_resp_field():
    with pytest.raises(ValueError) as t1:
        extract_json('{"not_response": {}}')
    assert "Missing or invalid 'response' field" in str(t1.value)
    with pytest.raises(ValueError) as t2:
        extract_json('{"response": 123}')
    assert "Missing or invalid 'response' field" in str(t2.value)