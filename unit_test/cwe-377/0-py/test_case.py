from tempfile import mktemp, TemporaryFile, NamedTemporaryFile

def write_results(results):
    '''
    create a temporary file and write "results" to it, return the file name
    '''    
    with NamedTemporaryFile() as f:
        f.write(results)
        return f.name
    
write_results('aaa')