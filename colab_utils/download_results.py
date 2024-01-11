import os
import pandas as pd
from datetime import datetime
import shutil
import argparse
from google.colab import files  # For triggering downloads in Colab

# Function to merge CSV files in a directory and save to a new CSV file
def merge_and_save_csv(export_dir, csv_folder):
    # Find all CSV files in the 'csv_folder'
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

    # Merge CSV files into a single DataFrame
    dfs = [pd.read_csv(os.path.join(csv_folder, file)) for file in csv_files]

    parent_dir_name = os.path.basename(os.path.dirname(csv_folder))
    merged_csv_path = os.path.join(export_dir, f"{parent_dir_name}.csv")

    if dfs:
        try:
            merged_df = pd.concat(dfs, ignore_index=True)
            merged_df.to_csv(merged_csv_path, index=False)
            return merged_csv_path
        except Exception as e:
            print(f'\nFailed to merge CSVs in {csv_folder}: {e}')
            return None
    else:
        print(f'\nNo CSVs found in {csv_folder}!')
        return None

def save_files(export_dir, file_folder):
    # Find all files in the folder
    files = [f for f in os.listdir(file_folder)]

    parent_dir_name = os.path.basename(os.path.dirname(file_folder))
    export_dir_path = os.path.join(export_dir, parent_dir_name)

    if files:
        try:
            # Create the export directory for files
            os.makedirs(export_dir_path, exist_ok=True)

            # Copy files to the export directory
            for file in files:
                source_path = os.path.join(file_folder, file)
                destination_path = os.path.join(export_dir_path, file)
                shutil.copy(source_path, destination_path)

            return export_dir_path
        except Exception as e:
            print(f'\nFailed to copy files from {file_folder}: {e}')
            return None
    else:
        print(f'\nNo files found in {file_folder}!')
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Empty specified directories and create .gitkeep files.')
    parser.add_argument('--target_directories', nargs='+', default=['files'], help='List of target directories to empty')

    args = parser.parse_args()

    # Function to process subdirectories and trigger downloads
    root_directory = 'results'
    subdirectories = [os.path.join(root_directory, folder) for folder in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, folder))]

    if subdirectories:
        # Create timestamped_export directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir = f'export/results_{timestamp}'
        os.makedirs(export_dir, exist_ok=True)

        for directory in subdirectories:
            csv_folders = [os.path.join(directory, folder) for folder in os.listdir(directory) if folder.endswith('csv')]
            for csv_folder in csv_folders:
                merge_and_save_csv(export_dir, csv_folder)

            for dir_id in args.target_directories:
                match_folders = [os.path.join(directory, folder) for folder in os.listdir(directory) if folder.endswith(str(dir_id))]
                for folder in match_folders:
                  save_files(export_dir, folder)

        # Create a zip file of the export directory
        archive_file = f'export/zip/results_{timestamp}'
        shutil.make_archive(archive_file, 'zip', export_dir)

        # Trigger download for the browser
        print(f'Created archive: {archive_file}.zip')

        # Trigger download for the browser
        files.download(f"{archive_file}.zip")
