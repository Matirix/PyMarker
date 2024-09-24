import os
import glob
import re
import shutil


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
        return None

    # Get the file with the latest modification time
    latest_file = max(filtered_files, key=os.path.getmtime)

    return latest_file


def move_latest_file_and_delete_folder(latest_file, folder_path, parent_folder):
    """
    Moves the latest file to the parent folder and deletes the folder.
    :param latest_file: The latest file that should be moved
    :param folder_path: Path to the folder where the file is located
    :param parent_folder: Path to the parent folder where the latest file should be moved
    """
    # Move the latest file to the parent folder
    destination = os.path.join(parent_folder, os.path.basename(latest_file))
    print(f"Moving: {latest_file} to {destination}")
    shutil.move(latest_file, destination)

    # Delete the folder after moving the file
    print(f"Deleting folder: {folder_path}")
    shutil.rmtree(folder_path)  # Removes the folder and its contents


if __name__ == "__main__":
    # Example usage
    folder_path = '/Users/Matthew/Downloads/Quiz1 Sep 23 2024 3'  # Replace with the folder path you want to scan
    parent_folder = os.path.dirname(folder_path)  # The parent folder where the latest file will be moved
    pattern = r'^\d{6}-\d{6}'  # Example pattern for files with a 12-digit start

    latest_file = get_latest_filtered_file(folder_path, pattern)

    if latest_file:
        move_latest_file_and_delete_folder(latest_file, folder_path, parent_folder)
    else:
        print("No matching files found.")
