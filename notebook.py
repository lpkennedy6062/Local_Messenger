# ICS 32
# Assignment #1: Diary
# Author: Aaron Imani
# v0.1.0
# notebook.py
'''Sets up notebook and diary class to be later utilized'''
import time
import json
from pathlib import Path
BASE_DIR = Path.home() / "Documents" / "ICS_32" / "a3-starter"
STORE_DIR = BASE_DIR / "store"


def load_user_data(username: str) -> dict:
    """Load contacts/messages for a user, or return default on error."""
    default = {"contacts": [], "messages": {}}
    path = STORE_DIR / f"{username}.json"
    try:
        test = path.read_text(encoding="utf-8")
        return json.loads(test)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_user_data(username: str, data: dict) -> None:
    """Save a user’s notebook, creating directories as needed."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    path = STORE_DIR / f"{username}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class NotebookFileError(Exception):
    """
    NotebookFileError is a custom exception handler that you
    should catch in your own code. It is raised when attempting
    to load or save Notebook objects to file the system.
    """


class IncorrectNotebookError(Exception):
    """
    NotebookError is a custom exception handler that you
    should catch in your own code. It is raised when
    attempting to deserialize a notebook file to a
    Notebook object.
    """


class Diary(dict):
    """

    The Diary class is responsible for working with individual user diaries.
    It currently supports two features: A timestamp property that is set upon
    instantiation and when the entry object is set and an entry property that
    stores the diary message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Diary properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        '''Sets up entry point'''
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        '''Returns self.entry'''
        return self._entry

    def set_time(self, tm: float):
        '''Sets time'''
        self._timestamp = tm
        dict.__setitem__(self, 'timestamp', tm)

    def get_time(self):
        '''Returns time'''
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Notebook:
    """Notebook is a class that can be used to manage a diary notebook."""

    def __init__(self, username: str, password: str, bio: str):
        """Creates a new Notebook object.
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            bio (str): The bio of the user.
        """
        self.username = username
        self.password = password
        self.bio = bio
        self._diaries = []

    def add_diary(self, diary: Diary) -> None:
        """Accepts a Diary object as parameter and appends to the diary list.
        Diaries are stored in a list object in the order they are added.
        So if multiple Diary objects are created, but added to the
        Profile in a different order, it is possible for the list to not
        be sorted by the Diary.timestamp property. So take caution as to
        how you implement your add_diary code.

        """
        self._diaries.append(diary)

    def del_diary(self, index: int) -> bool:
        """
        Removes a Diary at a given index and returns `True` if successful
        and `False` if an invalid index was supplied.
        To determine which diary to delete you must implement your own
        search operation on the diary returned from the get_diaries
        function to find the correct index.

        """
        try:
            del self._diaries[index]
            return True
        except IndexError:
            return False

    def get_diaries(self) -> list[Diary]:
        """Returns the list obj with all diaries added to the
        Notebook object"""
        return self._diaries

    def save(self, path: str) -> None:
        """
        Accepts an existing notebook file to save current
        instance of Notebook to the file system.
        Example usage:
        ```
        notebook = Notebook('jo)
        notebook.save('/path/to/file.json')
        ```
        Raises NotebookFileError, IncorrectNotebookError
        """
        p = Path(path)

        if p.exists() and p.suffix == '.json':
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(self.__dict__, f, indent=4)
            except Exception as ex:
                raise NotebookFileError(
                    "Error while attempting to process the notebook file.",
                    ex)from ex
        else:
            raise NotebookFileError("Invalid notebook file path or type")

    def load(self, path: str) -> None:
        """
        Populates the current instance of Notebook with data stored
        in a notebook file.
        Example usage:
        ```
        notebook = Notebook()
        notebook.load('/path/to/file.json')
        ```

        Raises NotebookFileError, IncorrectNotebookError
        """
        p = Path(path)

        if p.exists() and p.suffix == '.json':
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.bio = obj['bio']
                for diary_obj in obj['_diaries']:
                    diary = Diary(diary_obj['entry'], diary_obj['timestamp'])
                    self._diaries.append(diary)
                f.close()
            except Exception as ex:
                raise IncorrectNotebookError(ex) from ex
        else:
            raise NotebookFileError()
