# Get the latitude and longitude and date from the incoming YAML payload and return the temperature from the database called weather
@app.route('/api/temperature_for_location')
def temperature_for_location():
    db = sqlite3.connect('weather.db')
    yaml_payload = request.args.get('payload', None)