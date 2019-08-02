import json
import os
from urllib.parse import urljoin

import lxml.html


class FactorioModGetter:

    base_url = "https://mods.factorio.com"
    login_url = "login"
    mod_url = "mod"
    mods_tag_path = "tags.json"

    def __init__(self, username, password, session):
        self._username = username
        self._password = password
        self._session = session

        self._logged_in = False

    def login(self):
        url = urljoin(self.base_url, self.login_url)
        with self._session.get(url) as res:
            login_page = res.text

        doc = lxml.html.document_fromstring(login_page)
        csrf_token = doc.cssselect("#csrf_token")[0].get("value")

        data = {
            "csrf_token": csrf_token,
            "username": self._username,
            "password": self._password,
        }
        with self._session.post(url, data=data) as res:
            result = res.text
            if "Invalid username or password" in result:
                raise ValueError("Invalid username or password")
            if "Please pass the CAPTCHA" in result:
                raise ValueError("Trigger CAPTCHA! Wait or change IP.")
            self._logged_in = True

    def get_mod(self, mod_name, mod_tag):
        if not self._logged_in:
            self.login()

        url = urljoin(self.base_url, self.mod_url) + f"/{mod_name}"
        with self._session.get(url) as res:
            mod_page = res.text

        doc = lxml.html.document_fromstring(mod_page)
        href = doc.cssselect("i.fa-cloud-download")[0].getparent().get("href")

        tag = href.split("/")[-1]
        if tag == mod_tag:
            return False, ""

        url = urljoin(self.base_url, href)
        with self._session.get(url) as res:
            mod = res.content
        return mod, tag

    def get_mods(self, mod_names):
        if os.path.exists(self.mods_tag_path):
            with open(self.mods_tag_path) as f:
                mods_tag = json.load(f)
        else:
            mods_tag = {}

        for mod_name in mod_names:
            mod, tag = self.get_mod(mod_name, mods_tag.get(mod_name, ""))
            if mod:
                print(f"Synchronized {mod_name}")
                mods_tag[mod_name] = tag
                yield mod
            else:
                print(f"Tag matches, skip {mod_name}.")

        with open(self.mods_tag_path, "w") as f:
            json.dump(mods_tag, f, indent=4)
