# PickleToTextConverter.py
# -------------------------------------------------------------------------
# Origin: "Pickle to text.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   Converts Python pickle files into plain text to inspect serialized calcium
and pupil datasets manually before preprocessing.
#
# Inputs:
#   - .pkl files containing serialized trial data
#
# Outputs:
#   - .txt files containing decoded structures
#
# File Relationships:
#   - Used before TextToCSVConverter.
#
# Dependencies:
#   pickle, json, os
# -------------------------------------------------------------------------

import pickle
import pandas as pd
import os
import glob

def write_attribute(file, attribute, attr_value, level=0):
    indent = '  ' * level
    file.write(f"{indent}{attribute}:\n")
    if isinstance(attr_value, pd.DataFrame):
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            file.write(f"{indent}{attr_value.to_string()}\n")
    elif isinstance(attr_value, pd.Series):
        file.write(f"{indent}{attr_value.to_string()}\n")
    elif isinstance(attr_value, (list, tuple, set)):
        for item in attr_value:
            file.write(f"{indent}- {item}\n")
    elif isinstance(attr_value, dict):
        for key, value in attr_value.items():
            write_attribute(file, key, value, level+1)
    else:
        file.write(f"{indent}{attr_value}\n")
    file.write("\n")

def process_pickle_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = pickle.load(f)

    with open(output_file, 'w') as file:
        attributes = dir(data)
        for attribute in attributes:
            if not attribute.startswith('__'):
                attr_value = getattr(data, attribute)
                write_attribute(file, attribute, attr_value)

def process_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for input_file in glob.glob(os.path.join(input_folder, '*.pkl')):
        base_name = os.path.basename(input_file)
        output_file = os.path.join(output_folder, base_name.replace('.pkl', '.txt'))
        process_pickle_file(input_file, output_file)

# Example usage
input_folder = r'C:\Users\ASH213\Documents\Calcium activity\890'
output_folder = r'C:\Users\ASH213\Documents\Calcium activity\890'
process_folder(input_folder, output_folder)

print(f"All pickle files have been processed and saved to text files in {output_folder}")

