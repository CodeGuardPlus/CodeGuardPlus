from flask import Flask, request, redirect, session
import os
import subprocess
import sys
import sqlite3

app = Flask(__name__)

