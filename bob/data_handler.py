import json

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


# Reads bob-data.json file and returns its contents
def read_data_file():
    try:
        with open("bob-data.json", mode="r") as data_file:
            json_string = data_file.read()
            leet_data = json.loads(json_string)
            return leet_data
    except:
        pass


# dumps the data to .json file
def write_file(data):
    try:
        with open("bob-data.json", mode="w") as data_file:
            json_string = json.dumps(data)
            data_file.write(json_string)
        pass
    except:
        pass