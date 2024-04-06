#!/bin/bash
# Run get_commit_changes.sh
./get_commit_changes.sh
# Then run extract_data.py with Python
python3 extract_data.py
# Then split dataset
python3 split_dataset.py
echo "Script execution completed."