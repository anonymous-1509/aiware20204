#!/bin/bash

python3 extract_model_code.py --input_file_path generated_refactorings.jsonl --input_key 'input' --dir_prefix 'before_refactoring'

python3 extract_model_code.py --input_file_path generated_refactorings.jsonl --input_key 'generated_response' --dir_prefix 'codellama_refactoring'

python3 extract_model_code.py --input_file_path test.jsonl --input_key 'after' --dir_prefix 'developer_refactoring'

java -jar DesigniteJava.jar -i before_refactoring -o code_smells/before_refactoring_smells

java -jar DesigniteJava.jar -i codellama_refactoring -o code_smells/codellama_refactoring_smells

java -jar DesigniteJava.jar -i developer_refactoring -o code_smells/developer_refactoring_smells


python3 count_smells.py