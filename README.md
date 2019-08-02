# A project for localization of Factorio's mods

## Current state

### Supported mods

As I am using bob's mods, this project by default only supports bob's mod, 
although you can still use it personally to translate other mods.

The supported bob's mods are:

    boblibrary
    boblogistics
    bobpower
    bobplates
    bobwarfare
    bobinserters
    bobassembly
    bobtech
    bobmodules
    bobelectronics
    bobmining
    bobores
    bobrevamp
    bobvehicleequipment
    bobgreenhouse
    bobenemies
    clock
    bobclasses
    bobequipment

### Supported language

|Locale|Progress|Last translated date|Translator|
|------|--------|--------------------|----------|
|zh_CN |100%    |08/02/2019          |Sraw      |
|es_ES |0%      |Need contribution   |None      |
|fr    |0%      |Need contribution   |None      |
|ja    |0%      |Need contribution   |None      |
|ko    |0%      |Need contribution   |None      |
|ru    |0%      |Need contribution   |None      |
|uk    |0%      |Need contribution   |None      |

## To contribute translation

Please edit the `messages.po` file in `lang/your_language/LC_MESSAGES` directory.

You can upload the file or making a pull request.

Attention, as I may not know your language, so I will not check the translation.
If you find any translation related issue, please submit an issue and try to @ the translator.

## To use it personally

* `pipenv install --dev` to install all necessary packages.
* `python main.py sync your_username your_password` to pull all locales
  from Factorio's mod portal. The username and password are used to login the portal.
  You can specify which mods to pull in `mods.py` file.
* `python main.py extract your_locale` to extract all fields to 
  `lang/your_locale/LC_MESSAGES/messages.po`. 
  It will automatically update all new fields and comment outdated fields.
  A temporary `templates` directory will be created.
* Translate everything needed in `messages.po` file.
* `python main.py render your_locale` to render the translations in
  `locale/your_locale`
* Make a package by yourself and enjoy it :)

Usage:

```
usage: main.py [-h] {sync,extract,render,release} ...

positional arguments:
  {sync,extract,render,release}
                        Specify a subcommand
    sync                Sync modules.
    extract             extract translation content.
    render              render locale.
    release             release a mod.

optional arguments:
  -h, --help            show this help message and exit
```

sync:

```
usage: main.py sync [-h] [-p PROXY] username password

positional arguments:
  username              The username of your Factorio account.
  password              The password of your Factorio account.

optional arguments:
  -h, --help            show this help message and exit
  -p PROXY, --proxy PROXY
                        Specify a proxy to use. Format: http://host:port
```

extract:

```
usage: main.py extract [-h] locale

positional arguments:
  locale      Choose the locale template you want to generate.

optional arguments:
  -h, --help  show this help message and exit
```

render:

```
usage: main.py render [-h] locale

positional arguments:
  locale      Choose the locale you want to render.

optional arguments:
  -h, --help  show this help message and exit
```

release:

```
usage: main.py release [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## Gossip 

There is one known possible issue. As all the same strings will be merged in
`messages.po` file, it might cause some problems as the same strings can mean different
things in different situations.
