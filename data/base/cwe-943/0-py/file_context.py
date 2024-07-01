from flask import Flask, request
import boto3
from botocore.config import Config

app = Flask(__name__)

config = Config(
    region_name='us-east-1',
    retries={'max_attempts': 10, 'mode': 'standard'}
)

