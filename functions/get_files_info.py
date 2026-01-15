import os

def get_files_info(working_directory, directory="."):
    try:
        # Get the absolute path of the working directory and the target directory
        working_dir_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))
    
        valid_target_dir = os.path.commonpath([working_dir_abs_path, target_dir]) == working_dir_abs_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        for item in os.listdir(target_dir):
            item_name = os.path.join(target_dir, item)
            item_size = os.path.getsize(item_name)
            item_is_dir = os.path.isdir(item_name)        
            print(f'- {item}: file_size={item_size} bytes, is_dir={item_is_dir}')
    except Exception as e:
        return f'Error: {e}'