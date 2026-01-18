import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs_path, file_path_abs_path]) == working_dir_abs_path

        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path_abs_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs_path]
        if args is not None:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, cwd=working_dir_abs_path, timeout=30)
        
        if result.returncode != 0:
            error_msg = f"Process exited with code {result.returncode}"
            if result.stderr:
                error_msg += f"\nSTDERR: {result.stderr}"
            return error_msg
        
        if not result.stdout and not result.stderr:
            return "No output produced"
        
        output = []
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to pass to the Python file",
                items=types.Schema(type=types.Type.STRING),
                default=None
            ),
        },
    ),
)