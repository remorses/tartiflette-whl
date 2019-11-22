
def read(path):
    if path:
        with open(path) as f:
            return f.read()
    return ''