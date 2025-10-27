# TextToCSVConverter.py
# -------------------------------------------------------------------------
# Origin: "Text to csv.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   Converts structured text outputs into CSV format for use in downstream
preprocessing and analysis steps.
#
# Inputs:
#   - Text (.txt) files with numeric/labeled data
#
# Outputs:
#   - CSV files ready for analysis
#
# File Relationships:
#   - Complements PickleToTextConverter.
#
# Dependencies:
#   pandas, numpy, os
# -------------------------------------------------------------------------

import csv
import os
import glob


def process_text_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Remove the first three lines
    lines = lines[3:]

    # Find the index where 'bininfo:' appears and truncate the list
    for i, line in enumerate(lines):
        if 'bininfo:' in line:
            lines = lines[:i]
            break

    # Process lines to extract data
    processed_data = []
    for line in lines:
        trial = line[0:1].strip() if len(line) > 0 else ' '
        column2 = line[6:7].strip() if len(line) > 6 else ' '
        column3 = line[20:24].strip() if len(line) > 20 else ' '
        column4 = line[28:38].strip() if len(line) > 28 else ' '
        column5 = line[39:52].strip() if len(line) > 39 else ' '
        column6 = line[53:66].strip() if len(line) > 53 else ' '
        column7 = line[68:80].strip() if len(line) > 68 else ' '

        # Append extracted columns as a new row in the processed_data list
        processed_data.append([trial, column2, column3, column4, column5, column6, column7])

    # Define column headers
    headers = ['trial', 'stimcondition', 'bindist', 'time', 'calcium', 'bv', 'bold']

    # Write the data to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(processed_data)


def process_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all text files in the input folder
    for input_file in glob.glob(os.path.join(input_folder, '*.txt')):
        # Define the corresponding output file path
        base_name = os.path.basename(input_file)
        output_file = os.path.join(output_folder, base_name.replace('.txt', '.csv'))

        # Process the text file and save the output to the CSV file
        process_text_file(input_file, output_file)


# Example usage
input_folder = r'C:\Users\ASH213\Documents\Calcium activity\890'
output_folder = r'C:\Users\ASH213\Documents\Calcium activity\890'
process_folder(input_folder, output_folder)
