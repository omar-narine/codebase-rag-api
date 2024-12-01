import os

def remove_directory_contents(repo_dir_path):
    try:
        # List all the contents of the directory
        for item in os.listdir(repo_dir_path):
            item_path = os.path.join(repo_dir_path, item)

            if os.path.isdir(item_path):  # If it's a directory, recursively remove its contents
                remove_directory_contents(item_path)  # Recursively delete subdirectories
            else:
                os.remove(item_path)  # If it's a file, remove the file

        # After the directory is empty, remove it
        os.rmdir(repo_dir_path)
    
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False