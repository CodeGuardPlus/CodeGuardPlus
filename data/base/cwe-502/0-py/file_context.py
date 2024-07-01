#!/bin/python3
from flask import Flask, request, redirect
import os
import subprocess
import sys
import yaml
import sqlite3

app = Flask(__name__)

