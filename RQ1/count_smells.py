import os
import csv

CODE_SMELL_DIRECTORY = "code_smells"

def count_code_smells(directory):
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)

        if os.path.isdir(folder_path):
            design_smells_count = count_smells_in_file(os.path.join(folder_path, 'designCodeSmells.csv'))
            implementation_smells_count = count_smells_in_file(os.path.join(folder_path, 'implementationCodeSmells.csv'))

            total_smells = design_smells_count + implementation_smells_count
            print(f"Total code smells in {folder}: {total_smells}")

def count_smells_in_file(file_path):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            return sum(1 for row in reader)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0


count_code_smells(CODE_SMELL_DIRECTORY )
