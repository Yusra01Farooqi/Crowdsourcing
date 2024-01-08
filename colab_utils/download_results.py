import os
import pandas as pd
from google.colab import files  # For triggering downloads in Colab
from datetime import datetime
import shutil

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

def save_image_dir(export_dir, image_folder):
    # Find all image files in the 'image_folder'
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    parent_dir_name = os.path.basename(os.path.dirname(image_folder))
    export_dir_path = os.path.join(export_dir, f'{parent_dir_name}_images')

    if image_files:
        try:
            # Create the export directory for images
            os.makedirs(export_dir_path, exist_ok=True)

            # Copy images to the export directory
            for image_file in image_files:
                source_path = os.path.join(image_folder, image_file)
                destination_path = os.path.join(export_dir_path, image_file)
                shutil.copy(source_path, destination_path)

            return export_dir_path
        except Exception as e:
            print(f'\nFailed to copy images from {image_folder}: {e}')
            return None
    else:
        print(f'\nNo images found in {image_folder}!')
        return None

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

        image_folders = [os.path.join(directory, folder) for folder in os.listdir(directory) if folder.endswith('images')]
        for image_folder in image_folders:
            save_image_dir(export_dir, image_folder)

    # Create a zip file of the export directory
    archive_file=f'export/zip/results_{timestamp}'
    shutil.make_archive(archive_file, 'zip', export_dir)

    # Trigger download for the browser
    files.download(f"{archive_file}.zip")
