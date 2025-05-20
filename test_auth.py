from ds_messenger import DirectMessenger
dm = DirectMessenger(username='alice', password='password')
assert dm.authenticate(), "Authentication failed!"
print("✅ Logged in, token:", dm.token)
