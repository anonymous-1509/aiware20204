import json
import os
import argparse

def process_jsonl(input_file_path, input_key, dir_prefix):
    with open(input_file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                generated_response = data.get(input_key, "")
                commit_sha = data.get("commit_sha", "default_commit_sha")
                file_name = data.get("file_name", "default_name.java")

                # Preprocess the generated response
                refactored_code = preprocess_generated_response(generated_response)

                dir_path = os.path.join(dir_prefix, commit_sha)
                os.makedirs(dir_path, exist_ok=True)

                output_file_path = os.path.join(dir_path, file_name)
                with open(output_file_path, 'w') as java_file:
                    java_file.write(refactored_code)
            except Exception as e:
                print(f"An error occurred: {e}")

def preprocess_generated_response(response_text):
    marker = "Here's a refactored version of the code:"
    if marker in response_text:
        # Keep only the part after the marker
        return response_text.split(marker)[-1]
    else:
        # If the marker is not found, return the original text
        return response_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON lines and extract specified data.')
    parser.add_argument('--input_file_path', type=str, help='The path to the input JSONL file.')
    parser.add_argument('--input_key', type=str, default='input', help='The key to extract input from JSON.')
    parser.add_argument('--dir_prefix', type=str, default='before_refactoring', help='The prefix for the directory path.')
    
    args = parser.parse_args()

    process_jsonl(args.input_file_path, args.input_key, args.dir_prefix)