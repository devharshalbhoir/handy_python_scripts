import os
import pycodestyle
import sys

# Define the folder you want to search
# Get the path to the directory where the script is saved
folder = os.path.dirname(os.path.realpath(__file__))
# folder = "path/to/your/folder"

# Create a StyleGuide object with the PEP8 standards, ignoring E501
style = pycodestyle.StyleGuide(ignore=["E501"])

# Find all .py files in the folder and any subfolders
python_files = []
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith(".py"):
            python_files.append(os.path.join(root, file))

# Check each file for PEP8 compliance
error_count = 0
for filename in python_files:
    result = style.check_files([filename])
    if result.total_errors != 0:
        error_count += result.total_errors
        print("Errors in file", filename)
        for error in result.messages:
            print("-", error)

# Print the results
if error_count == 0:
    print("All Python files in", folder, "conform to PEP8 standards.")
else:
    print("There were", error_count, "errors in Python files in", folder)
    sys.exit(1)

