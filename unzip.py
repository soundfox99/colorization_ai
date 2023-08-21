import os
import zipfile

def unzip_files(source_dir, destination_dir):
    for file_name in os.listdir(source_dir):
        if file_name.endswith('.zip'):
            file_path = os.path.join(source_dir, file_name)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_dir)


if __name__ == "__main__":

    source_dir = "E:/ml_color_data/training_data/zip_files"
    dest_dir = "E:/ml_color_data/training_data/raw_data"


    unzip_files(source_dir, dest_dir)