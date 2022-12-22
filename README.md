# Slack File Grabber
This script allows you to download files from a JSON backup of your Slack workspace. It can handle download interruptions and resume the download from where it left off. The script also generates a mapping file that contains the UUIDs of the downloaded files, which you can use to search through the downloaded files.

To use the script, place the JSON files from an unzipped Slack backup in the `input` directory and run the following command:
`python main.py --input_directory ./input`

Alternatively, you can use an existing mapping file to download the files:

`python main.py --mapping_file output_mapping.json`

You can also specify both the `input_directory` and `mapping_file` arguments if you want to generate the mapping file and download the files in a single command. In this case, the `input_directory` argument will take precedence and the mapping file will be generated from the JSON files in that directory.

`python main.py --input_directory ./input --mapping_file output_mapping.json`

### Prerequisites
* Python 3.6 or higher
* The following Python packages:
* `requests`
* `tqdm`

### Note
This project was mainly created for my personal purposes and for another project I am working on.
