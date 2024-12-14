from pathlib import Path


def delete_directory(output_folder_path: Path):
    # Iterate through all files and directories in the folder
    for item in output_folder_path.iterdir():
        if item.is_file():
            item.unlink()  # Delete the file
        elif item.is_dir():
            delete_directory(item)  # Recursively delete contents
            item.rmdir()  # Remove the empty directory
