import os
import shutil


def rename_and_move_file(folder_path: str):
    # Get the folder name
    folder_name = os.path.basename(folder_path)


    file_name = os.listdir(folder_path)[0]  # Modify if there are multiple files
    # print(os.listdir(folder_path))
    file_path = os.path.join(folder_path, file_name)

    # Create a new file name by prepending the folder name
    new_file_name = f"{folder_name}_{file_name}"
    new_file_path = os.path.join(os.path.dirname(folder_path), new_file_name)

    try:
        # Rename and move the file
        shutil.move(file_path, new_file_path)
        print(f"File renamed and moved to: {new_file_path}")
    except PermissionError as e:
        print(f"Permission error while processing {file_name}: {e}")
    except Exception as e:
        print(f"Error while processing {file_name}: {e}")


if __name__ == '__main__':
    p_directory = '/Users/Matthew/Downloads/Grading Materials from Matthew Puyat/2024_LE_EECS_F_3421__3_B_EN_A_LECT_01-Project_Fall2024_CLO1_CLO5-3247616 copy'

    # Iterate over all items in the parent directory
    for folder in os.listdir(p_directory):
        folder_path = os.path.join(p_directory, folder)
        # print(folder_path)

        # Check if the item is a directory (not a file)
        if os.path.isdir(folder_path):
            rename_and_move_file(folder_path)