import os
import json
import urllib.parse
import uuid

output_mapping = {}

def parse_json_in_directory(directory_path, output_mapping):
    # get a list of all files and directories in the given directory
    file_list = os.listdir(directory_path)

    # go through each file and directory
    for file_or_directory in file_list:
        # get the full path of the file or directory
        file_or_directory_path = os.path.join(directory_path, file_or_directory)

        # if it is a directory, recursively call this function on it
        if os.path.isdir(file_or_directory_path):
            parse_json_in_directory(file_or_directory_path, output_mapping)
        # if it is a file, check if it is a JSON file and parse it if it is
        elif os.path.isfile(file_or_directory_path):
            # check if the file has a .json extension
            if file_or_directory_path.endswith('.json'):
                # open the file and parse the JSON data
                with open(file_or_directory_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    # go through each object in the JSON data
                    for obj in json_data:
                        # check if the object has a "files" field
                        if 'files' in obj:
                            # go through each file in the "files" field
                            for file in obj['files']:
                                # check if the file has a "url_private_download" field
                                if 'url_private_download' in file:
                                    # unescape the URL and add it to the output mapping
                                    unescaped_url = urllib.parse.unquote(file['url_private_download'])
                                    uuid_key = str(uuid.uuid1())
                                    output_mapping[uuid_key] = {
                                        "link": unescaped_url,
                                        "path": file_or_directory_path
                                    }