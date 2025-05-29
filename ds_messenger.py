# ds_messenger.py
# Starter code for assignment 2 in ICS 32 Programming in Python
# Replace the following placeholders with your information.
# Liam
# lpkenned@uci.edu
# 81845142
'''Sets up the Messaging and connections'''
import socket
import time
from ds_protocol import make_auth, make_directmessage, make_fetch, extract_json
from notebook import load_user_data, save_user_data


class DirectMessage:
    '''Format for the specific Direct Message function'''
    def __init__(self) -> None:
        self.recipient = None
        self.message = None
        self.sender = None
        self.timestamp = None


class DirectMessenger:
    '''Support code for the Messenger'''
    def __init__(self, host='127.0.0.1',
                 port=3001, username=None, password=None) -> None:
        self.token = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.token = None
        self._sock = None
        self._in = None
        self._out = None
        self._local = load_user_data(self.username)

    def connect(self) -> None:
        '''Connects to the host/port while allowing for reading and writing'''
        self._sock = socket.create_connection((self.host, self.port))
        self._in = self._sock.makefile('r')
        self._out = self._sock.makefile('w')

    def authenticate(self, username=None, password=None) -> bool:
        '''Authenticates the messenger with the username and the password'''
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        self.connect()
        msg = make_auth(self.username, self.password)
        self._out.write(msg + '\r\n')
        self._out.flush()

        raw = self._in.readline()
        resp = extract_json(raw)

        if resp.type == 'ok':
            self.token = resp.token
            self._local = load_user_data(self.username)
            return True
        return False

    def send_msg(self, message: str, recipient: str) -> bool:
        '''Returns true if message successfully sent, false if send failed'''
        ts = time.time()
        msg = make_directmessage(self.token, message, recipient, ts)
        self._out.write(msg + '\r\n')
        self._out.flush()

        resp = extract_json(self._in.readline())
        ok = resp.type == 'ok'
        if ok:
            if recipient not in self._local['contacts']:
                self._local['contacts'].append(recipient)
            self._local['messages'].setdefault(recipient, []).append({
                'sender': self.username, 'recipient': recipient,
                'message': message, 'timestamp': str(ts)})
            save_user_data(self.username, self._local)
        return ok

    @property
    def local(self) -> dict:
        '''Read only accoss to notebook'''
        return self._local

    @local.setter
    def local(self, new_local) -> None:
        '''Allows tests to modify local'''
        self._local = new_local

    def retrieve_new(self) -> list:
        '''Returns list of DirectMessage objects containing all new messages'''
        self._out.write(make_fetch(self.token, 'unread') + '\r\n')
        self._out.flush()
        resp = extract_json(self._in.readline())

        out = []
        for m in resp.messages or []:
            dm = DirectMessage()
            dm.sender = m.get('from')
            dm.recipient = None
            dm.message = m.get('message')
            dm.timestamp = m.get('timestamp')
            out.append(dm)

            peer = dm.sender
            if peer not in self._local['contacts']:
                self._local['contacts'].append(peer)
            self._local['messages'].setdefault(peer, []).append({
                "sender": peer, 'recipient': self.username,
                'message': dm.message, 'timestamp': dm.timestamp})
        save_user_data(self.username, self._local)
        return out

    def retrieve_all(self) -> list:
        '''Returns list of DirectMessage objects containing all messages'''
        self._out.write(make_fetch(self.token, 'all') + '\r\n')
        self._out.flush()
        resp = extract_json(self._in.readline())
        out = []

        for m in resp.messages or []:
            dm = DirectMessage()
            dm.sender = m.get('from')
            dm.recipient = m.get('recipient')
            dm.message = m.get('message')
            dm.timestamp = m.get('timestamp')
            out.append(dm)
        return out
