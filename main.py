import argparse
import json
import os
import re
import shutil
import zipfile
from io import BytesIO

import babel
import requests
from babel import UnknownLocaleError, localedata
from babel.messages.frontend import CommandLineInterface

from modules.factorio import FactorioModGetter
from modules.localization import Localizer
from mods import mod_names


def sync_mod_locale(_mod_getter, _mod_names):
    for mod in _mod_getter.get_mods(_mod_names):
        mod_zip = zipfile.ZipFile(BytesIO(mod))

        regex = re.compile(r".*(locale/.*\.cfg)")
        for _info in mod_zip.infolist():
            matched = regex.match(_info.orig_filename)
            if matched is not None:
                filename = matched.group(1)
                _info.filename = filename
                mod_zip.extract(_info)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


if __name__ == '__main__':
    # Here we monkeypatch this to completely disable python_format.
    # noinspection PyPropertyAccess
    babel.messages.catalog.Message.python_format = False

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="Specify a subcommand", dest="subcommand", required=True)

    parser_sync = subparsers.add_parser('sync', help='Sync modules.')
    parser_sync.add_argument('username',
                             help='The username(not email address) of your Factorio account.')
    parser_sync.add_argument('password',
                             help='The password of your Factorio account.')
    parser_sync.add_argument('-p', '--proxy',
                             help="Specify a proxy to use. Format: http://host:port")

    parser_extract = subparsers.add_parser('extract', help='extract translation content.')
    parser_extract.add_argument('locale',
                                help='Choose the locale template you want to generate.')

    parser_render = subparsers.add_parser('render', help='render locale.')
    parser_render.add_argument('locale',
                               help='Choose the locale you want to render.')

    parser_release = subparsers.add_parser('release', help="release a mod.")

    args = parser.parse_args()

    if args.subcommand == "sync":
        username = args.username
        password = args.password

        session = requests.Session()
        if args.proxy:
            proxy = args.proxy
            proxies = {
                "http": proxy,
                "https": proxy
            }
            session.proxies.update(proxies)
        mod_getter = FactorioModGetter(username, password, session)
        try:
            sync_mod_locale(mod_getter, mod_names)
        except ValueError as e:
            print(e)
    elif args.subcommand in ["extract", "render"]:
        locale = args.locale
        if not localedata.exists(locale):
            raise UnknownLocaleError(locale)
        if args.subcommand == "extract":
            localizer = Localizer()
            localizer.generate_template("locale/en")
            CommandLineInterface().run(
                ['pybabel', 'extract', '-F', 'babel.cfg', '-o', 'messages.pot', '.'])
            if os.path.exists(f"lang/{locale}"):
                CommandLineInterface().run(
                    ['pybabel', 'update', '-i', 'messages.pot', '-d', 'lang', '-l', locale])
            else:
                CommandLineInterface().run(
                    ['pybabel', 'init', '-i', 'messages.pot', '-d', 'lang', '-l', locale])
            os.remove("messages.pot")
        else:
            CommandLineInterface().run(
                ['pybabel', 'compile', '-f', '-d', 'lang'])
            localizer = Localizer()
            localizer.render_locale(locale)
    elif args.subcommand == "release":
        with open("info.json") as f:
            info = json.load(f)
        version = info["version"]

        dir_name = "bobsmodslocale" + "_" + version

        shutil.rmtree(dir_name, ignore_errors=True)
        os.makedirs(dir_name, exist_ok=True)
        shutil.copytree("locale", os.path.join(dir_name, "locale"))
        shutil.copy2("info.json", dir_name)

        with zipfile.ZipFile(dir_name + '.zip', 'w', zipfile.ZIP_DEFLATED) as f:
            zipdir(dir_name, f)
        shutil.rmtree(dir_name, ignore_errors=True)
