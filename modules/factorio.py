import json
import os
from urllib.parse import urljoin
from requests import Response, Session


class FactorioModGetter:

    download_base_url = "https://mods.factorio.com"
    login_url = "https://auth.factorio.com/api-login"
    info_url = "https://mods.factorio.com/api/mods"
    mods_sha1_path = "sha1.json"

    def __init__(self, username, password, session):
        self._username = username
        self._password = password
        self._session: Session = session

        self._token = None

    def login(self):
        login_url = self.login_url

        payload = {
            "username": self._username,
            "password": self._password
        }
        with self._session.post(login_url, data=payload) as res:
            code = res.status_code
            if code != 200:
                raise ValueError("Invalid username or password")
            self._token = res.json()[0]

    def get_mod(self, mod_name, mod_sha1):
        url = "/".join((self.info_url, mod_name))
        with self._session.get(url) as res:
            info = res.json()
            sha1 = info["releases"][-1]["sha1"]
            download_url = info["releases"][-1]["download_url"]

        if mod_sha1 == sha1:
            return False, ""

        if self._token is None:
            self.login()
        url = urljoin(self.download_base_url, download_url)
        payload = {
            "username": self._username,
            "token": self._token
        }
        res: Response
        with self._session.get(url, params=payload) as res:
            mod = res.content
        return mod, sha1

    def get_mods(self, mod_names):
        if os.path.exists(self.mods_sha1_path):
            with open(self.mods_sha1_path) as f:
                mods_sha1 = json.load(f)
        else:
            mods_sha1 = {}

        for mod_name in mod_names:
            mod, sha1 = self.get_mod(mod_name, mods_sha1.get(mod_name, ""))
            if mod:
                print(f"Synchronized {mod_name}")
                mods_sha1[mod_name] = sha1
                yield mod
            else:
                print(f"Tag matches, skip {mod_name}.")

        with open(self.mods_sha1_path, "w") as f:
            json.dump(mods_sha1, f, indent=4)
