Direct Messaging Chat

By Liam Kennedy

A Python/Tkinter client for the DS Direct Messaging Protocol.
Implements a JSON over TCP protocol to authenticate, send, and fetch messages from a local server, with local storage of contacts and chat history.


Includes:
- DSP Protocol: Builds and parses JSON commands for functions like authenticate, directmessage, and fetch.
- Storage: File automatically saves contacts and message history to disk.
- Tkinter GUI: Includes window with contacts list, live checkins for new messages, and ability to show send/receive messages with visuals.
- Testers: Files look to test overall functionality covering ds_messenger and ds_protocol.
- Server: Connects locally to itself to allow for the ability to send messages back and forth.
- Notebook: Hosts background diary and class for notebook's functionality acting as the program's backbone. 
