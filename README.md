# IAESTE Now

The IAESTE map is a website facilitating the discovery of people, events and
couches in IAESTE on a geographic basis. It is built using modern web
technologies, specifically:

* Flask
* SQLAlchemy
* Google Maps APIs
* jQuery

## Dependencies

Make sure Python 3 is installed, and install Flask and SQLAlchemy through the
pip python package manager:
```sh
sudo pip install Flask SQLAlchemy
```

Make sure you install with `pip3` if Python 2 is your default version (likely).

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
