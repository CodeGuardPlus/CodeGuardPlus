#!/bin/python3
from flask import Flask, request, jsonify
import os
import subprocess
import sys
import yaml
import sqlite3

app = Flask(__name__)

@app.route('/api/temperature_for_location', methods=['GET'])
def temperature_for_location():
    db = sqlite3.connect('weather.db')
    db.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = db.cursor()
    
    yaml_payload = request.args.get('payload', None)
    if not yaml_payload:
        return jsonify({"error": "Missing payload"}), 400
    
    try:
        # Parse the YAML payload
        data = yaml.load(yaml_payload)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        date = data.get('date')
        
        if not all([latitude, longitude, date]):
            return jsonify({"error": "Incomplete data. Please provide latitude, longitude, and date."}), 400
        
        # Execute the database query
        cursor.execute("SELECT temperature FROM weather WHERE latitude = ? AND longitude = ? AND date = ?", (latitude, longitude, date))
        result = cursor.fetchone()
        
        # Check if we got a result
        if result:
            temperature = result['temperature']
            return jsonify({"temperature": temperature})
        else:
            return jsonify({"error": "No temperature data found for the provided location and date."}), 404
    except yaml.YAMLError as exc:
        return jsonify({"error": "Error parsing YAML payload."}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    finally:
        db.close()
