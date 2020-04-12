def write_file(path,text):
    """
    path = string
    text = string

    write the string to the file in the path
    """
    with open(path, 'w') as file:
        file.write(text)

def read_file(path):
    """
    return one string with the entire file
    """
    content_str = ""
    try:
        with open(path, 'r') as file:
            for line in file:
                content_str += line
    except:
        pass
    return content_str