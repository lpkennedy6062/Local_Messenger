from ds_messenger import DirectMessenger
from notebook import load_user_data

import time, json, os
def test_newadd():
    store = os.path.expanduser('~/.ds_store/alice.json')
    try: os.remove(store)
    except OSError: pass

    alice = DirectMessenger(username='alice', password='password')
    assert alice.authenticate()

    msgs = alice.retrieve_new()
    print("First retrieve_new() returned:", msgs)

    data = load_user_data('alice')
    print("On disk after empty fetch:", json.dumps(data, indent=2))

    from ds_messenger import DirectMessenger as DM2
    bob = DM2(username='bob', password='password')
    bob.authenticate()
    assert bob.send_msg("hey alice", "alice")

    time.sleep(0.1)

    new2 = alice.retrieve_new()
    print("Second retrieve_new() returned:", [(d.sender,d.message) for d in new2])

    data2 = load_user_data('alice')
    print("On disk after message fetch:", json.dumps(data2, indent=2))
