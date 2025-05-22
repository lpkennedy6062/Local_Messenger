from ds_messenger import DirectMessenger
from notebook import load_user_data

import time, json, os

# Make sure we start with no file
store = os.path.expanduser('~/.ds_store/alice.json')
try: os.remove(store)
except OSError: pass

# 1) Alice logs in and retrieves nothing
alice = DirectMessenger(username='alice', password='password')
assert alice.authenticate()

# If Bob has sent nothing yet, retrieve_new() should be empty
msgs = alice.retrieve_new()
print("First retrieve_new() returned:", msgs)
# Check that file now exists and has the right shape
data = load_user_data('alice')
print("On disk after empty fetch:", json.dumps(data, indent=2))

# 2) Have Bob send something
from ds_messenger import DirectMessenger as DM2
bob = DM2(username='bob', password='password')
bob.authenticate()
assert bob.send_msg("hey alice", "alice")

time.sleep(0.1)

# 3) Alice fetches again
new2 = alice.retrieve_new()
print("Second retrieve_new() returned:", [(d.sender,d.message) for d in new2])

# 4) Inspect disk
data2 = load_user_data('alice')
print("On disk after message fetch:", json.dumps(data2, indent=2))
