import os

def get_files_info(working_directory, directory="."):
    try:
        #get the full path joing the absolute path of the working directory and the passed directory argument
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            return(f'Error: "{directory}" is not a directory')
        name_files = os.listdir(target_dir)

        final_lines = []
        for name in name_files:
            file_size = os.path.getsize(os.path.join(target_dir, name))
            is_directory = os.path.isdir(os.path.join(target_dir, name))
            final_lines.append(f"- {name}: file_size={file_size} bytes, is_dir={is_directory}")
        return "\n".join(final_lines)
    except Exception as e:
        return f"Error: {str(e)}" 