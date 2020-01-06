from datetime import datetime

from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def GetObject():
    return []


def GetAccessURL():
    return "accessurl goes here"


def read():
    return []
