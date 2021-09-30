# Python Anleitung

## Installation von Python

* Unter Unix Have a look: https://docs.python-guide.org/starting/install3/linux/
* Unter Mac Have a look: https://docs.python-guide.org/starting/install3/osx/
* Unter Windows Have a look: https://docs.python-guide.org/starting

## Aufbau einer virtuellen Umgebung

* Unix/Mac: `python3.8 -m venv .venv` # .venv/.env sind Usus, allerdings ist der Name beliebig
* Widnows: `python -m venv c:\path\to\myenv`

Details sfinden sich hier: https://docs.python.org/3/library/venv.html

## Aktivierung der virtuellen Umgebung

* Unix/Mac: `source .venv/bin/activate`
* Windows: `.venv\Scripts\activate.bat`

## Deaktivierung der virtuellen Umgebung

* Unix/Mac/Windows: `deactivate`

## Installation von Paketen

Einzelpaket: `pip install pandas`
Mehrer Pakte aus einer `requirements.txt` (wie hier) oder aber aus einer `setup.py`: `pip install -r requirements.txt`

## Unittests mit Pytest ausführen

Unix/Mac/Windows: `pytest -vv -s`

## SDK Workshop für Python

Bau des [Pythonskripts](./create_bucket.py) zu erstellen eines Bucket.
Aufbau der [Unittests](./test_create_bucket.py)