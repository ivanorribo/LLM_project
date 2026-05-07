import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, absolute_file_path]) != working_dir_abs:
            return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(absolute_file_path):
            return(f'Error: "{file_path}" does not exist or is not a regular file')
        if not file_path.endswith(".py"):
            return(f'Error: "{file_path}" is not a Python file')
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)
        process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        final_string = ""
        if process.returncode != 0:
            final_string += (f"Process exited with code {process.returncode}")
        if not process.stdout and not process.stderr:
            final_string += (f"No output produced")
        else:
            if process.stdout:
                final_string += f"STDOUT:\n{process.stdout}\n"
            if process.stderr:
                final_string += f"STDERR:\n{process.stderr}\n"
        return final_string
    except Exception as e:
        return (f"Error: executing Python file: {e}")
    
