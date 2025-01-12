import json
from typing import List
from collections import UserList
from pathlib import Path
import os

class AccountCredentials:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

class AccountsList(UserList[AccountCredentials]):
    def __init__(self, accounts: list) -> None:
        data = []
        for each in accounts:
            data.append(AccountCredentials(**each))
        self.data: List[AccountCredentials] = data

def Load_accounts(file="accounts.json"):
    "Load all accounts from a specified json file"
    return AccountsList(**json.load(open(file)))

class CacheStore:
    def __init__(self, name, path_store = '.genshin_cookies') -> None:
        self.name = f"{name}_cache.json"
        self.path = Path(os.path.join(os.getcwd(), path_store, self.name))
        self.loaded = None
        if not self.path.parent.is_dir():
            self.path.parent.mkdir(exist_ok=True)
        elif self.path.exists():
            with open(self.path) as f:
                try:
                    self.loaded = json.load(f)
                except json.JSONDecodeError:
                    self.loaded = None

    def _store_data(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f)

    def load(self):
        return self.loaded

    def dump(self, new_data):
        self._store_data(new_data)