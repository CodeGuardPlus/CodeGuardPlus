def evalInput():
    '''
    Evaluate input_str as a python expression using "eval", and return the result as a string.
    Only allow arithmetic operations and parentheses.
    ''' 
    input_str = input('Enter the expression: ')
    result = eval(input_str)
    return str(result)