import json
import sys


# Reads the ranks.txt and returns it contents as a list
def read_ranks_file():
    ranks = []
    file = open('ranks.txt')
    for line in file:
        # strip removes all whitsespaces from end and beginning
        line = line.strip()
        ranks.append(line)
    file.close()
    return ranks


# Reads .json file and returns its contents
def read_json_file(file_name):
    try:
        with open(file_name, mode="r") as data_file:
            json_string = data_file.read()
            data = json.loads(json_string)
            return data
    except:
        print(sys.exc_info()[0])


# dumps the data to .json file
def write_json_file(data, filename):
    try:
        with open(filename, mode="w") as data_file:
            json_string = json.dumps(data)
            data_file.write(json_string)
        pass
    except:
        print(sys.exc_info()[0])

