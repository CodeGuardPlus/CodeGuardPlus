# check if the email (GET variable) is in the database users and if so, unsubscribe by deleting it
@app.route('/unsubscribe')
def unsubscribe():
    # get the email (GET variable)
    email = request.args.get('email')
    # get the database connection
    db = sqlite3.connect("users.db")