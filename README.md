# Capritools 2

Capritools 2 is a set of extremely useful tools for passing around information and intelligence for [EVE Online](https://www.eveonline.com/). It's written entirely in Django.

The site is hosted at [skyride.org](https://skyride.org/), but since this handles a lot of opsec information you're welcome to set up your own installation.


## Features

* Dscan ([Example](https://skyride.org/dscan/WQ45PVY/))
* Localscan ([Example](https://skyride.org/local/J2ojF5v/))
* Pastebin ([Example](https://skyride.org/paste/7yjyiMu/))
* [Moon Goo Profitability](https://skyride.org/quickmath/moongoo/) and [Implant Sets](https://skyride.org/quickmath/implants/)

You can now also log in, and view/delete any scans or pastes you've entered.


## Planned Features

* Fleet tracking via API


## Installation

This application is still very much under development, however these instructions should work.

```
virtualenv .
git clone https://github.com/skyride/capritools-2.git
source bin/activate
cd capritools-2
pip install -r requirements.txt
cp capritools/local_settings.example capritools/local_settings.py
```

Go to capritools/local_settings.py and configure it

```
python manage.py migrate
python import.py
```

#### Celery
We use Celery as a backend to get prices and eventually do fleet tracking. Running this command in a screen session should do the job.

```
celery worker -A capritools -B -c 4
```
