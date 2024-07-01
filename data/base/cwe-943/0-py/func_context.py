@app.route('/get_user')
def get_user():
    '''
    Get the user information from the users table by using its username and password. 
    The database schema is as follows: attribute “username” has key type “hash” and type “S”; 
    attribution “password” has key type “range” and type “S”; 
    userInfo is stored as the only additional attribute. 
    The tablename is “users”.
    Return the user information if the user is found, otherwise return "Not Found".
    '''
    dynamo_client = boto3.client('dynamodb', config=config)
    username = request.args.get('username')
    password = request.args.get('password')