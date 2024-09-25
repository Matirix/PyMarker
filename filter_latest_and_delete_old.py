import os
import glob
import re


def get_latest_filtered_file(folder_path, pattern):
    """
    Function to get the latest file that matches the 12-digit pattern from a specified folder.
    :param folder_path: Path to the folder
    :param pattern: Regex pattern for the first 12 digits in the filename
    :return: The latest file in the folder that matches the pattern
    """
    # Compile the regex pattern to match the first 12 digits
    regex = re.compile(pattern)

    # Use glob to find all files in the folder
    files = glob.glob(os.path.join(folder_path, '*'))  # Adjust the wildcard if necessary

    # Filter files based on the first 12 digits in the filename
    filtered_files = [f for f in files if regex.match(os.path.basename(f))]

    if not filtered_files:
        print("No matching files found in the specified folder.")
        return None, []

    # Get the file with the latest modification time
    latest_file = max(filtered_files, key=os.path.getmtime)

    return latest_file, filtered_files


def delete_old_files(latest_file, all_files):
    """
    Deletes all files except the latest one.
    :param latest_file: The file that should not be deleted
    :param all_files: List of all files matching the pattern
    """
    for file in all_files:
        if file != latest_file:
            print(f"Deleting: {file}")
            os.remove(file)  # Deletes the file


if __name__ == "__main__":
    # Example usage
    folder_path = '/Users/Matthew/Downloads/Quiz1 Sep 23 2024 2'  # Replace with the folder path you want to scan
    pattern = r'.*A0\d{10}.*'  # Example pattern for files with 12-digit start
    latest_file, filtered_files = get_latest_filtered_file(folder_path, pattern)

    if latest_file:
        print(f"The latest matching file is: {latest_file}")
        # Now delete the old files
        delete_old_files(latest_file, filtered_files)
    else:
        print("No matching files found to delete.")
