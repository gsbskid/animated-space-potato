def format_path(path) : 
    '''
    Function to format the path

    Args :
        1) path : str : path to format

    Returns :
        1) str : formatted path
    
    '''

    path = path.replace('\n' , '')
    path = path.replace('\t' , '')
    path = path.replace(' ' , '')

    return path