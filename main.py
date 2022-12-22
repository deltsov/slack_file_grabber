import os
import json
import re
import requests
from json_parser import parse_json_in_directory
from tqdm import tqdm
import argparse



def main(input_directory=None, mapping_file=None):
    if input_directory is not None:
        # parse the JSON files and create the output mapping
        output_mapping = {}
        parse_json_in_directory(input_directory, output_mapping)

        # save the output mapping to a JSON file
        with open('output_mapping.json', 'w') as output_file:
            json.dump(output_mapping, output_file)
        # set the input_mapping variable to the output_mapping
        input_mapping = output_mapping
        
    elif mapping_file is not None:
        # load the input mapping from the JSON file
        with open(mapping_file, 'r') as input_file:
            input_mapping = json.load(input_file)
    else:
        raise ValueError('Either input_directory or mapping_file must be provided')

    # create a directory to save the files
    download_directory = './downloads'
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Initialize an empty list to store the UUIDs
    uuids = []

    # Iterate through the files in the download directory
    for file in os.listdir(download_directory):
        # Extract the UUID from the filename using a regular expression
        match = re.search(r'_(.{8}-.{4}-.{4}-.{4}-.{12})', file)
        if match:
            # If a match is found, add the UUID to the list
            uuids.append(match.group(1))

    # use tqdm to log the global progress
    for uuid_key, link_and_path in tqdm(input_mapping.items(), total=len(input_mapping), desc='Processing files'):
        # skip the file if the UUID is in the list of UUIDs
        if uuid_key in uuids:
          continue
        # get the link and path from the dictionary
        link = link_and_path['link']
        path = link_and_path['path']

        # use a regular expression to extract the file extension from the link
        file_extension_match = re.search(r'\.\w{3,4}($|\?)', link)
        if file_extension_match:
            file_extension = file_extension_match.group(0).replace('?', '')
        else:
            file_extension = ''

        # extract the file name from the link
        file_name = link.split('/')[-1]
        file_name = file_name.split('?')[0]  # remove the query string from the file name

        #check if the file name is too long and if so, truncate it
        if len(file_name) > 32:
            file_name = file_name[:32]


        # create the final file name in the desired format
        final_file_name = f"{file_name}_{uuid_key}{file_extension}"

        # make a GET request to the link using tqdm to log the download progress
        with tqdm(desc=f'Downloading {final_file_name}', unit='B', unit_scale=True, leave=False) as pbar:
            response = requests.get(link, stream=True)
            # check if the request was successful
            if response.status_code == 200:
                # get the file data from the response
                file_data = response.content

                # create the file path to save the file
                file_path = os.path.join(download_directory, final_file_name)

                # write the file data to disk
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive
                            file.write(chunk)
                            pbar.update(1024)
            else:
                    print(f'Error downloading {final_file_name} - {response.status_code}')
                    print(response.text)
                    print()
if __name__ == '__main__':
    # create an argument parser
    parser = argparse.ArgumentParser()
    # add the optional input_directory and mapping_file arguments
    parser.add_argument('--input_directory', help='Directory containing the JSON files')
    parser.add_argument('--mapping_file', help='JSON file containing the mapping information')
    # parse the arguments
    args = parser.parse_args()
    # pass the arguments to the main function
    main(input_directory=args.input_directory, mapping_file=args.mapping_file)