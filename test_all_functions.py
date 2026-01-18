from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info

working_directory = "."

print(get_file_content(working_directory, 'main.py'))
print(write_file(working_directory, 'main.txt', 'hello'))
print(run_python_file(working_directory, 'main.py'))
print(get_files_info(working_directory, 'pkg'))