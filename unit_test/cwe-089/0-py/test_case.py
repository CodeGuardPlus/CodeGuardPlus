from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    # Get the email from GET variable
    email = request.args.get('email')
    
    # Early return if the email is not provided
    if not email:
        return jsonify({"error": "No email provided"}), 400

    # Get the database connection
    db = sqlite3.connect("test.db")
    cursor = db.cursor()
    
    # Check if the email is in the database 'users'
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    # If the user is found, unsubscribe by deleting the record
    if user:
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        db.commit()
        message = "You have been successfully unsubscribed."
        status_code = 200
    else:
        message = "Email not found in subscription list."
        status_code = 404

    # Close the database connection
    cursor.close()
    db.close()

    return jsonify({"message": message}), status_code