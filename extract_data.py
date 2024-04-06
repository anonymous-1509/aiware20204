import os
import json
import zipfile

def extract_java_source_code(zip_path, output_file, overall_data, repository):
    print(f"Processing zip file: {zip_path}")
    extract_path = os.path.splitext(zip_path)[0]
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        print(f"Extracted to {extract_path}")

        extract_path_dir = extract_path + '/separated'

        for commit_sha_folder in os.listdir(extract_path_dir):
            commit_path = os.path.join(extract_path_dir, commit_sha_folder)
            if os.path.isdir(commit_path):
                #print(f"Processing commit SHA folder: {commit_sha_folder}")
                prev_path = os.path.join(commit_path, 'previous')
                curr_path = os.path.join(commit_path, 'current')

                matched_files = find_matched_java_files(prev_path, curr_path)
                for file in matched_files:
                    prev_file_path = os.path.join(prev_path, file)
                    curr_file_path = os.path.join(curr_path, file)

                    prev_code = read_java_files(prev_file_path)
                    curr_code = read_java_files(curr_file_path)

                    if prev_code and curr_code:
                        # Fetch refactoring types for this commit SHA
                        refactoring_types = overall_data.get(commit_sha_folder, {})

                        # Construct the JSON data with commit_sha, refactoring_types, before, and after
                        json_data = json.dumps({
                            'project': repository,
                            'commit_sha': commit_sha_folder,
                            'file_name': file,
                            'refactoring_types': refactoring_types,
                            'before': prev_code,
                            'after': curr_code
                        })
                        output_file.write(json_data + '\n')
                        #print(f"Written data for file: {file} in commit SHA folder: {commit_sha_folder}")

        os.system(f'rm -rf {extract_path}')
        print(f"Deleted extracted directory: {extract_path}")


def find_matched_java_files(prev_path, curr_path):
    prev_files = set(f for f in os.listdir(prev_path) if f.endswith('.java'))
    curr_files = set(f for f in os.listdir(curr_path) if f.endswith('.java'))
    return prev_files.intersection(curr_files)


def read_overall_data(overall_zip_path):
    overall_data = {}
    with zipfile.ZipFile(overall_zip_path, 'r') as zip_ref:
        zip_ref.extractall()
        for project_json in os.listdir("overall/Overall"):
            print(f"Processing {project_json}")
            with open(f"overall/Overall/{project_json}", 'r') as file:
                project_data = json.load(file)
                for commit_sha, commit_data in project_data.items():
                    # Check if refactorings is not empty, refactoring churn is at least 90% of the insertions, and insertions is greater than 0
                    if commit_data['insertions'] > 0 and commit_data['refactoring_churn'] / commit_data['insertions'] >= 0.9 and commit_data['refactorings']:
                        operations = commit_data.get('operations', {})
                        # Filter out refactoring types with a count of 0
                        used_refactorings = {k: v for k, v in operations.items() if v > 0}
                        overall_data[commit_sha] = used_refactorings
    return overall_data


def read_java_files(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        print(f"Skipped non-UTF-8 file: {file_path}")
        return None

def main():
    data_dir = 'projects'
    output_filename = 'java_code_changes.jsonl'

    overall_data = read_overall_data('Overall.zip')

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for project in os.listdir(data_dir):
            print(f"Processing project: {project}")
            project_path = os.path.join(data_dir, project)
            if os.path.isdir(project_path):
                zip_file = f'{project_path}/separated_{project}.zip'
                if os.path.exists(zip_file):
                    extract_java_source_code(zip_file, output_file, overall_data, project)
                else:
                    print(f"Zip file not found: {zip_file}")
            else:
                print(f"Not a directory: {project_path}")

if __name__ == '__main__':
    main()
