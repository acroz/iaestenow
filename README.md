# IAESTE Now

IAESTE Now is a website facilitating the discovery of people, events and
couches in IAESTE on a geographic basis. It is built using modern web
technologies, specifically:

* Flask
* SQLAlchemy
* Google Maps APIs
* jQuery

## Dependencies

Make sure Python 3 is installed, and install some dependencies through the pip
python package manager:
```sh
sudo pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF requests twitter
```

Make sure you install with `pip3` if Python 2 is your default version (likely).

## Setup

API keys for services being scraped, in particular Facebook and Twitter, must
be generated and added to a settings file called `settings.json`. Copy the
template `settings-template.json` and fill in as described below.

### Application Secret

Generate a long, random string, such as with the command:

```sh
python -c "import random; import string; \
print(''.join([random.choice(string.ascii_letters + string.digits) for i in range(60)]))"
```

and save it to the `secret_key` entry in `settings.json`.

### Facebook

Generate a Facebook app at https://developers.facebook.com/apps/, and add the
application ID and secret to the settings.json file.

### Twitter

Generate an application key at https://dev.twitter.com/apps/new, and add the
application key and secret to the settings.json file.

## Running the Development Server

Run the development server with:
```sh
./runserver.py
```

If you get the error:
```
/usr/bin/env: python3: No such file or directory
```
you probably do not have python3 installed.

At the moment, the development server is set up to generate a new database and
populate it with some content when run. When the Python files are modified and
saved, the server will automatically reload (and crash if there is an error).
