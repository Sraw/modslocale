# A project for localization of Factorio's mods

## Usage

First, use `pipenv install --dev` to install all necessary packages.

Then, use `python main.py sync your_username your_password` to pull all locales
from Factorio's mod portal.

You can specify which mods to pull in `mods.py` file.

Next, use `python main.py extract your_locale` to extract all fields to 
`lang/your_locale/LC_MESSAGES/messages.po`.

In this progress, a temporary `templates` directory will be created.

Finally, after you translate everything needed in `messages.po` file,
use `python main.py render your_locale` to render the translations in
`locale/your_locale`

## Gossip 

For now, it only supports `zh_CN`. To add more locales, please contact me or
directly make pull requests.

There is one known possible issue. As all the same strings will be merged in
`messages.po` file, it might cause some problems as the same strings can mean different
things in different situations.
