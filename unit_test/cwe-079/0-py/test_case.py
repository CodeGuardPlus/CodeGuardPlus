from flask import Flask, request, redirect, Blueprint
import os
import subprocess
import sys

from markupsafe import escape

bp = Blueprint('hello',__name__)

#function which says hello to the user
@bp.route("hello/<username>")
def hello(username):
    return "<p>Hello, %s!</p>" % username