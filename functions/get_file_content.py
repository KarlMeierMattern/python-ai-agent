import os
from google.genai import types

MAX_CHARACTERS = 10000

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs_path, file_path_abs_path]) == working_dir_abs_path

        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs_path, 'r') as file:
            content = file.read(MAX_CHARACTERS)
            if len(content) == MAX_CHARACTERS and file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
            return content
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get the content from, relative to the working directory",
            ),
        },
    ),
)