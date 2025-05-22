from ds_protocol import make_auth, extract_json, ServerResponse

def test_auth_round_trip():
    # simulate server’s ok response
    raw = '{"response":{"type":"ok","message":"hi","token":"tkn123"}}'
    resp = extract_json(raw)
    assert isinstance(resp, ServerResponse)
    assert resp.type == "ok"
    assert resp.token == "tkn123"
    assert resp.messages is None
