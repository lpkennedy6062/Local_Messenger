# a2.py
# Liam
# lpkenned@uci.edu
# 81845142
import tkinter as tk
import time
from tkinter import ttk, filedialog, simpledialog
from typing import Text
from notebook import load_user_data, save_user_data
from ds_messenger import DirectMessenger


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback = None, add_user_callback = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._add_user_callback = add_user_callback
        self._contacts = []
        # After all initialization is complete, call the _draw method to pack the widgets into the Body instance
        self._draw()

    def node_select(self, _event):
        self.message_editor.config(state='normal')
        self.message_editor.delete('1.0', tk.END)
        self.message_editor.config(state='disabled')
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.message_editor.config(state = 'normal')
        self.message_editor.insert('end', message + '\n', 'entry-right')
        self.message_editor.config(state = 'disabled')

    def insert_contact_message(self, message:str):
        self.message_editor.config(state = 'normal')
        self.message_editor.insert('end', message + '\n', 'entry-left')
        self.message_editor.config(state = 'disabled')

    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.entry_editor.delete(1.0, tk.END)
        self.entry_editor.insert(1.0, text)

    def _draw(self):
        #left
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

        # contacts tree
        self.posts_tree = ttk.Treeview(posts_frame, selectmode='browse')
        self.posts_tree.heading("#0", text="Contacts")
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=(5,0))
        # Add user button
        add_btn = tk.Button(posts_frame, text = 'Add User', command=self._add_user_callback)
        add_btn.pack(fill=tk.X, side = tk.BOTTOM, padx = 5, pady = (5,0))
        
        #right and message display
        message_frame = tk.Frame(self)
        message_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)

        hist_frame = tk.Frame(message_frame)
        hist_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        self.message_editor = tk.Text(hist_frame, state = 'disabled', wrap='word')
        
        self.message_editor.tag_configure('entry-right', justify='right')
        self.message_editor.tag_configure('entry-left', justify='left')
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        hist_scroll = tk.Scrollbar(hist_frame, command=self.message_editor.yview)
        self.message_editor['yscrollcommand'] = hist_scroll.set
        hist_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # entry / scroll removed master=self
        entry_frame = tk.Frame(message_frame)
        entry_frame.pack(fill=tk.X, side=tk.TOP, expand=False, pady=(5,0))

        self.entry_editor = tk.Text(entry_frame, wrap = 'word', height=5)
        
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.X, expand = True)

        #entry_scroll = tk.Scrollbar(entry_frame, command=self.entry_editor.yview)

        #self.entry_editor['yscrollcommand'] = entry_scroll.set
        #entry_scroll.pack(side=tk.RIGHT, fill=tk.Y)

class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command = self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack(pady=(10,0))
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        
        self.server = '127.0.0.1'
        self.username = 'alice'
        self.password = 'password'
        
        from ds_messenger import DirectMessenger
        self.direct_messenger = DirectMessenger(host=self.server, port = 3001, username = self.username, password = self.password)
        if not self.direct_messenger.authenticate():
            tk.messagebox.showerror("Login failed", "Cound not connect with those creds")
            self.root.destroy()
            return
        
        self._draw()
        self._local = load_user_data(self.username)
        for c in self._local['contacts']:
            if c not in self.body._contacts:
                self.body.insert_contact(c)
        # You must implement this! You must configure and instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!
        # After all initialization is complete, call the _draw method to pack the widgets into the root frame
        #self.body.insert_contact("studentexw23") adding one example student.

    def send_message(self):
        # You must implement this!
        print("DEBUG: send_message() called; recipient=", self.recipient)
        text = self.body.get_text_entry().strip()
        print("DEBUG: text=", repr(text))
        if not text or not self.recipient:
            return
        ok = self.direct_messenger.send_msg(text, self.recipient)
        if ok:
            self.body.insert_user_message(text)
            self._local['messages'].setdefault(self.recipient,[]).append({"sender": self.username, "recipient": self.recipient, "message":   text, "timestamp": str(time.time())})
            save_user_data(self.username, self._local)
            self.body.set_text_entry("")
        else:
            tk.messagebox.showerror("Send failed", f"Cound not send to {self.recipient}")

    def add_contact(self):
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body methods to add the contact to your contact list
        new = tk.simpledialog.askstring("Add Contact", "Username:")
        if not new or new in self._local['contacts']:
            return
        pwd = tk.simpledialog.askstring(f"Password for {new}", f"Enter password to register or authenticate '{new}':", show="*")
        if pwd is None:
            return
        temp = DirectMessenger(host=self.server, port=3001, username=new, password=pwd)

        if temp.authenticate():
            self.body.insert_contact(new)
            self._local['contacts'].append(new)
            self._local['messages'][new] = []
            save_user_data(self.username, self._local)
        else:
            tk.messagebox.showerror("Error", f"I could not register user {new}")
        '''if new:
            self.body.insert_contact(new)
            if new not in self._local['contacts']:
                self._local['contacts'].append(new)
                self._local['messages'][new] = []
                save_user_data(self.username, self._local)'''

    def recipient_selected(self, recipient):
        self.recipient = recipient

        self.body.message_editor.config(state='normal')
        self.body.message_editor.delete('1.0', tk.END)

        history = self._local['messages'].get(recipient, [])
        for msg in history:
            if msg['sender'] == self.username:
                self.body.insert_user_message(msg['message'])
            else:
                self.body.insert_contact_message(msg['message'])

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        # You must configure and instantiate your DirectMessenger instance after this line.

    def publish(self, message:str):
        if self.recipient == self.username:
            self.body.insert_user_message(message)
        else:
            self.body.insert_contact_message(message)

    def check_new(self):
        new = self.direct_messenger.retrieve_new()
        for dm in new:
            sender = dm.sender
            msg = dm.message

            if sender not in self._local['contacts']:
                self._local['contacts'].append(sender)
                self.body.insert_contact(sender)
            self._local['messages'].setdefault(sender, []).append({'sender': sender, 'recipient': self.username, 'message': msg, 'timestamp': dm.timestamp})
            if sender == self.recipient:
                self.body.insert_contact_message(msg)
        save_user_data(self.username, self._local)
        self.root.after(2000, app.check_new)
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)
        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, recipient_selected_callback=self.recipient_selected, add_user_callback=self.add_contact)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        row1 = tk.Frame(master)
        row1.pack(fill='x', padx=5, pady=2)
        tk.Label(row1, text="Server:").pack(side='left')
        self.server_entry = tk.Entry(row1)
        self.server_entry.insert(0, "127.0.0.1")
        self.server_entry.pack(side='right', fill='x', expand=True)

        row2 = tk.Frame(master)
        row2.pack(fill='x', padx=5, pady=2)
        tk.Label(row2, text="Username:").pack(side='left')
        self.user_entry = tk.Entry(row2)
        self.user_entry.pack(side='right', fill='x', expand=True)

        row3 = tk.Frame(master)
        row3.pack(fill='x', padx=5, pady=2)
        tk.Label(row3, text="Password:").pack(side='left')
        self.pw_entry = tk.Entry(row3, show='*')
        self.pw_entry.pack(side='right', fill='x', expand=True)
        return self.user_entry

    def apply(self):
        self.server = self.server_entry.get().strip()
        self.username = self.user_entry.get().strip()
        self.password = self.pw_entry.get()

if __name__ == "__main__":
    '''server = '127.0.0.1'
    username = 'alice'
    password = 'password'''
    root = tk.Tk()
    root.withdraw()

    dlg = LoginDialog(root, title="Login to DS Server")
    if not getattr(dlg, "username", ""):
        root.destroy()
        exit(1)

    dm = DirectMessenger(host=dlg.server, port = 3001, username = dlg.username, password = dlg.password)
    if not dm.authenticate():
        print("Login failed - check server/info")
        root.destroy()
        exit(1)
    
    root.deiconify()
    root.title("Direct Messenger")
    root.geometry("800x600")
    app = MainApp(root)
    app.direct_messenger = dm

    def check():
        app.check_new()
        root.after(2000, check)
    root.after(2000, check)
    root.mainloop()
'''
    main.geometry("720x480")
    main.option_add('*tearOff', False)

    app = MainApp(main)

    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
'''


'''def_quit(self) -> None:
        if tkinter.messagebox.asokcancel(title='Quit', message = "Really quit?):
            self.destroy'''