#!/bin/bash

BASE_DIR="projects"

# Define project names derived from URLs
declare -a project_names=("dubbo" "skywalking" "flink" "rocketmq" "hadoop" "pulsar" "druid" "cassandra" "jmeter" "tomcat")

IFS=',' read -ra urls <<< "$(cat repositories.txt)"

# Ensure the projects directory exists
mkdir -p "$BASE_DIR"

# Iterate through the URLs and remove leading/trailing double quotes
for url in "${urls[@]}"; do
    url="${url%\"}"   # Remove leading double quote
    url="${url#\"}"   # Remove trailing double quote
    echo "$url"

    REPO_URL=$url  # Replace with your repository URL
    # Clone the repository
    git clone "$REPO_URL"

    CLONE_DIR=$(basename "$REPO_URL" .git)

    cd "$CLONE_DIR" || exit

    # Get the list of commit SHAs in reverse chronological order
    commit_shas=$(git rev-list --reverse HEAD)

    # Create directories for storing changes
    mkdir -p separated

    # Iterate over each commit SHA
    for sha in $commit_shas; do
        # Create directories for the current commit
        commit_dir_previous="separated/$sha/previous"
        commit_dir_current="separated/$sha/current"

        mkdir -p "$commit_dir_previous"
        mkdir -p "$commit_dir_current"

        # Checkout the commit (forceful)
        git checkout -f "$sha"

        # Get the changed files in the commit
        changed_files=$(git diff-tree --no-commit-id --name-only -r "$sha")

        # Copy the changed files to the target folder
        for file in $changed_files; do
            echo $file
            cp "$file" "$commit_dir_current"
        done

        # Copy all files from the previous commit to the previous directory
        git checkout -f "$sha^"  # Checkout the previous commit
        for file in $changed_files; do
            echo $file
            cp "$file" "$commit_dir_previous"
        done

        echo "Stored changes for commit $sha"
    done

    # Return to the original branch
    git checkout -

    # Zip the separated directory
    zip -r "separated_$CLONE_DIR.zip" separated

    # Optionally, remove the separated directory after zipping to save space
    rm -rf separated
    
    echo "Script execution completed."
    cd ../
done

# Move the specified project directories into the projects directory
for project_name in "${project_names[@]}"; do
    if [ -d "$project_name" ]; then
        mv "$project_name" "$BASE_DIR/"
    fi
done

<<<<<<< HEAD
echo "Specified directories moved to $BASE_DIR."
=======
echo "Specified directories moved to $BASE_DIR."
>>>>>>> b30d475 (Data Collection)
