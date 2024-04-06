import json
import random
from collections import defaultdict

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def save_jsonl(data, file_path):
    with open(file_path, 'w') as file:
        for entry in data:
            json.dump(entry, file)
            file.write('\n')

def split_data(input_file_path, train_file_path, test_file_path, validation_file_path, split_ratio=0.8, validation_split_ratio=0.1):
    # Load data
    data = load_jsonl(input_file_path)
    
    # Group data by 'commit_sha'
    grouped_data = defaultdict(list)
    for entry in data:
        commit_sha = entry.get('commit_sha', '')
        grouped_data[commit_sha].append(entry)
    
    # Shuffle the groups
    grouped_data_items = list(grouped_data.items())
    random.shuffle(grouped_data_items)
    
    # Calculate the split index for train and test
    split_index = int(len(grouped_data_items) * split_ratio)
    
    # Further calculate the split index for train and validation within the train dataset
    train_validation_split_index = int(split_index * (1 - validation_split_ratio))
    
    # Split the data
    train_groups = grouped_data_items[:train_validation_split_index]
    validation_groups = grouped_data_items[train_validation_split_index:split_index]
    test_groups = grouped_data_items[split_index:]
    
    # Flatten the groups back into lists
    train_data = [item for group in train_groups for item in group[1]]
    validation_data = [item for group in validation_groups for item in group[1]]
    test_data = [item for group in test_groups for item in group[1]]
    
    # Save the split data
    save_jsonl(train_data, train_file_path)
    save_jsonl(validation_data, validation_file_path)
    save_jsonl(test_data, test_file_path)
    
# Define file paths
input_file_path = 'java_code_changes.jsonl'
train_file_path = 'RQ2/train.jsonl'
validation_file_path = 'RQ2/validation.jsonl'
test_file_path = 'RQ1/test.jsonl'

# Execute data splitting
split_data(input_file_path, train_file_path, test_file_path, validation_file_path)

