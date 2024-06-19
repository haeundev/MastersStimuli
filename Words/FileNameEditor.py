import os
import glob

# Function to recursively find all wav files in a directory
def find_wav_files(directory):
    wav_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                wav_files.append(os.path.join(root, file))
    return wav_files

# Function to rename wav files
def rename_wav_files(directory):
    wav_files = find_wav_files(directory)
    for old_file_path in wav_files:
        dirname = os.path.dirname(old_file_path)
        filename = os.path.basename(old_file_path)
        new_filename = filename.replace("Masker_Words_", "")  # Modify the filename as needed
        new_file_path = os.path.join(dirname, new_filename)
        os.rename(old_file_path, new_file_path)
        print(f"Renamed: {old_file_path} -> {new_file_path}")

# Change directory to the desired starting directory
starting_directory = "./"
os.chdir(starting_directory)

# Call the function to rename wav files
rename_wav_files(starting_directory)
