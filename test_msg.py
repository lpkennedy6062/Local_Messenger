from ds_messenger import DirectMessenger
import time

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
