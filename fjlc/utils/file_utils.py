def count_lines(file_name):
    try:
        f = open(file_name)
        count = sum(1 for line in f)
        f.close()
        return count
    except IOError:
        raise IOError


def read_entire_file_into_string(file_name):
    with open(file_name) as f:
        return f.read()


def write_to_file(file, data):
    with open(file) as f:
        f.write(data)
