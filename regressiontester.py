import os
from batcher import batcher

def process_files(directory):
    file_data = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            result = batcher(filepath)
            file_data.append((filename, result))

    for filename, result in file_data:
        print(f"File: {filename}")
        print(f"Result: {result}")

if __name__ == "__main__":
    current_directory = "HD5ytesting_nvda"
    process_files(current_directory)
