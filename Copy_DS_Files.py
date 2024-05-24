import shutil
import os

# Path to the source file in the current directory
source_file = 'hanford.dat'

# Base directory where the destination folders are located
base_dir = './pflo_Input/Hem/'
n = 90 #600 #22 #300
# Iterate from 1 to 250 to construct folder names and copy the file
for i in range(1, n+1):
    # Construct the destination folder path
    dest_folder = os.path.join(base_dir, f'run_{i}')

    # Ensure the destination folder exists, create it if not
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Construct the full path to where the file will be copied
    dest_path = os.path.join(dest_folder, source_file)

    # Copy the file
    shutil.copy(source_file, dest_path)

print("File has been copied to all specified folders.")
