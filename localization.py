import os
import re

from babel.support import Translations
from jinja2 import FileSystemLoader, Environment


class Localizer:

    def __init__(self):
        self.regex = re.compile(r"=(.*)")
        self.output_dir = "templates"

        loader = FileSystemLoader("templates")
        extensions = ['jinja2.ext.i18n']
        self.env = Environment(extensions=extensions, loader=loader)
        self.locale_dir = "lang"

    def generate_template(self, root):
        files = os.listdir(root)
        files = [os.path.join(root, file) for file in files if file.endswith(".cfg")]

        os.makedirs(self.output_dir, exist_ok=True)
        for file in files:
            with open(file) as f:
                content = f.read()

            content = content.replace('"', '\\"')
            content = self.regex.sub(r'={{ _("\g<1>")|replace("\\n","\\\\n") }}', content)
            basename = os.path.basename(file)
            basename = ".".join([basename.split(".")[0], "jinja2"])

            output_path = os.path.join(self.output_dir, basename)
            with open(output_path, "w") as f:
                f.write(content)

    def render_locale(self, locale):
        env = self.env

        list_of_desired_locales = [locale]
        translations = Translations.load(self.locale_dir, list_of_desired_locales)

        env.uninstall_gettext_translations(None)
        env.install_gettext_translations(translations)

        templates = env.list_templates()

        output_dir = f"locale/{locale.replace('_', '-')}"
        os.makedirs(output_dir, exist_ok=True)
        for template_name in templates:
            template = env.get_template(template_name)
            output_name = ".".join([template_name.split(".")[0], "cfg"])
            template.stream().dump(os.path.join(output_dir, output_name))
