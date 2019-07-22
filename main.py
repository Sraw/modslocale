import argparse
import os
import re
import zipfile
from io import BytesIO

import babel
from babel.messages.frontend import CommandLineInterface

from modules.factorio import FactorioModGetter
from modules.localization import Localizer
from mods import mod_names


def sync_mod_locale(_mod_getter, _mod_names):
    for mod_name in _mod_names:
        mod = _mod_getter.get_mod(mod_name)

        mod_zip = zipfile.ZipFile(BytesIO(mod))

        regex = re.compile(r".*(locale/.*\.cfg)")
        for info in mod_zip.infolist():
            matched = regex.match(info.orig_filename)
            if matched is not None:
                filename = matched.group(1)
                info.filename = filename
                mod_zip.extract(info)


if __name__ == '__main__':
    babel.messages.catalog.Message.python_format = False

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_sync = subparsers.add_parser('sync', help='Sync modules.')
    parser_sync.add_argument('username',
                             help='The username of your Factorio account.')
    parser_sync.add_argument('password',
                             help='The password of your Factorio account.')
    parser_sync.set_defaults(sync=True)

    parser_extract = subparsers.add_parser('extract', help='extract translation content.')
    parser_extract.add_argument('locale', choices=["zh_CN", "ja", "de", "fr", "ru", "uk", "ko"],
                                help='Choose the locale template you want to generate.')
    parser_extract.set_defaults(extract=True)

    parser_render = subparsers.add_parser('render', help='render locale.')
    parser_render.add_argument('locale', choices=["zh_CN"],
                               help='Choose the locale you want to render.')
    parser_render.set_defaults(render=True)

    args = parser.parse_args()

    if "sync" in args and args.sync:
        username = args.username
        password = args.password
        mod_getter = FactorioModGetter(username, password)
        sync_mod_locale(mod_getter, mod_names)
    elif "extract" in args and args.extract:
        locale = args.locale
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
    elif "render" in args and args.render:
        CommandLineInterface().run(
            ['pybabel', 'compile', '-f', '-d', 'lang'])
        localizer = Localizer()
        locale = args.locale
        localizer.render_locale(locale)
    else:
        parser.print_help()
