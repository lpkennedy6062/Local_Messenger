from ds_messenger import DirectMessenger
import time

# 1) Start two clients: Alice and Bob
alice = DirectMessenger(username='alice', password='password')
bob   = DirectMessenger(username='bob',   password='password')

assert alice.authenticate(), "Alice login failed"
assert bob.authenticate(),   "Bob login failed"

# 2) Alice sends Bob a message
ok = alice.send_msg("Hello Bob!", "bob")
print("Alice→Bob send OK:", ok)

# Give the server a moment
time.sleep(0.1)

# 3) Bob retrieves new messages
new = bob.retrieve_new()
print("Bob got messages:", [(dm.sender, dm.message) for dm in new])

# 4) Alice retrieves all to see her outgoing
all_msgs = alice.retrieve_all()
print("Alice conversation:", [(dm.sender or alice.username, dm.message) for dm in all_msgs])
