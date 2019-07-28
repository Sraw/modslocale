from urllib.parse import urljoin

import lxml.html


class FactorioModGetter:

    base_url = "https://mods.factorio.com"
    login_url = "login"
    mod_url = "mod"

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
        with self._session.post(url, data=data):
            self._logged_in = True

    def get_mod(self, mod_name):
        if not self._logged_in:
            self.login()

        url = urljoin(self.base_url, self.mod_url) + f"/{mod_name}"
        with self._session.get(url) as res:
            mod_page = res.text

        doc = lxml.html.document_fromstring(mod_page)
        href = doc.cssselect("i.fa-cloud-download")[0].getparent().get("href")

        url = urljoin(self.base_url, href)
        with self._session.get(url) as res:
            mod = res.content
        return mod
