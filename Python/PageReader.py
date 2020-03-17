

def read_file(path):
    content_str = str()
    with open(path, 'r') as file:
        for line in file:
            content_str += line
    return content_str
