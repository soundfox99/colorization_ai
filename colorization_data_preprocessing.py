# Imported Python Libraries
import os
from PIL import Image
import shutil
import random
import time
import random
import re
import concurrent.futures

# Imported Third Party Libraries
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from tqdm import tqdm

# Global Variable Definations
MAX_WIDTH = 1400
MAX_LENGTH = 2048

# Function Definations
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size

def create_image_dimensions_histogram(directory):

    image_counter = 0
    dimensions = []
    for root, dirs, files in os.walk(directory):
        for filename in tqdm(files):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')) and (filename.split('.')[0] != "final"):
                # Iterate thought all the image files and get their dimensions 
                image_path = os.path.join(root, filename)
                image_dimensions = get_image_dimensions(image_path)
                
                # Only keep images that are between the specific ranges
                image_counter += 1
                if ((image_dimensions[0] <= MAX_WIDTH) and (image_dimensions[1] <= MAX_LENGTH)):
                    dimensions.append(image_dimensions)
                else:
                    #if (filename.split(".")[0] == "01"):
                    print(f"{root + filename}: {image_dimensions}")

    # Print the amount of images that fit the criteria
    print(image_counter)
    print(len(dimensions))
    print((len(dimensions)/image_counter) * 100)
    width, height = zip(*dimensions)

    # Plot the histogram using plolty
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=width, name='Width', opacity=0.75))
    fig.add_trace(go.Histogram(x=height, name='Height', opacity=0.75))

    fig.update_layout(
        title_text='Image Dimensions Histogram',
        xaxis=dict(title='Dimension'),
        yaxis=dict(title='Count'),
        bargap=0.2,
        bargroupgap=0.1
    )

    fig.show()

def pad_image(image_path, target_size):
    # Open the image
    image = Image.open(image_path)

    # Get the current size
    width, height = image.size

    # Calculate the padding size
    padding_width = max(target_size[0] - width, 0)
    padding_height = max(target_size[1] - height, 0)

    # Calculate the left, top, right, and bottom padding
    left = padding_width // 2
    top = padding_height // 2
    right = padding_width - left
    bottom = padding_height - top

    # Pad the image with black pixels
    padded_image = Image.new(image.mode, target_size, color='black')
    padded_image.paste(image, (left, top))

    # Save and replace the original image
    os.remove(image_path)
    padded_image.save(image_path)


def copy_and_rename_pictures(source_dir, dest_dir, prefix="image_", start_index=1, training_data_split=0.8):
    
    # Delete and remake the destination directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Count the amount of examples so we know how much to make training and validation
    num_inputs = count_files_in_directory(source_dir) + start_index
    num_train_data = (int) (num_inputs * training_data_split)


    index = start_index
    switch_to_validation = False
    for root, dirs, files in os.walk(source_dir):

        first_page = True
        first_page_path = ""

        # Determine if we should switch to validation and reset index
        if (index > num_train_data):
            switch_to_validation = True
            index = 1


        if not switch_to_validation:
            alt_dest_dir = dest_dir + "/training"
        else:
            alt_dest_dir = dest_dir + "/validation"

        # Make the destination directories
        input_1_dir = input_2_dir = output_dir = dest_dir
        input_1_dir = alt_dest_dir + "/Input_1/"
        input_2_dir = alt_dest_dir + "/Input_2/"
        output_dir = alt_dest_dir + "/Output/"

        if not os.path.exists(input_1_dir): os.makedirs(input_1_dir)
        if not os.path.exists(input_2_dir): os.makedirs(input_2_dir)
        if not os.path.exists(output_dir): os.makedirs(output_dir)

        for filename in tqdm(files):

            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')) and (filename.split('.')[0] != "final"):
                source_path = os.path.join(root, filename)

                # Copy the image if it is smaller or equal to the image limitations
                image_dimensions = get_image_dimensions(source_path)
                if ((image_dimensions[0] <= MAX_WIDTH) and (image_dimensions[1] <= MAX_LENGTH)):
                    if first_page:
                        first_page_path = source_path

                        first_page = False
                        continue
                    else:
                        
                        dest_filename = f"{prefix}{index}{os.path.splitext(filename)[1]}"
                        
                        # Copy the files into their correct folders
                        output_path = os.path.join(output_dir, dest_filename)
                        input_2_path = os.path.join(input_2_dir, dest_filename)
                        input_1_path = os.path.join(input_1_dir, dest_filename)

                        shutil.copyfile(first_page_path, input_1_path)
                        shutil.copyfile(source_path, output_path)

                        with Image.open(source_path) as img:
                            input_2_image = img.convert("L")
                            input_2_image.save(input_2_path)
                        
                        index += 1

    return


                    


def pad_images(directory):
    # Iterate through images and add black padding to them
    for root, dirs, files in os.walk(directory):
        for filename in tqdm(files):
            target_size = (MAX_WIDTH, MAX_LENGTH)
            path = os.path.join(root, filename)
            pad_image(path, target_size)

def process_image(path):
    target_size = (MAX_WIDTH, MAX_LENGTH)
    pad_image(path, target_size)

def pad_images_parallel(directory):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_paths = []
        for root, dirs, files in os.walk(directory):
            for filename in files:
                path = os.path.join(root, filename)
                image_paths.append(path)
        
        list(tqdm(executor.map(process_image, image_paths), total=len(image_paths)))

def count_files_in_directory(directory_path):
    file_count = 0
    for root, dirs, files in os.walk(directory_path):
        file_count += len(files)
    return file_count

def shuffle_data(source_dir, dest_dir):

    # Remove and remake the destination directories
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    training_input1 = count_files_in_directory(source_dir + "/training/Input_1")
    training_input2 = count_files_in_directory(source_dir + "/training/Input_2")
    training_output = count_files_in_directory(source_dir + "/training/Output")

    # If the amount of images are not equal just return
    if not (training_input1 == training_input2 == training_output):
        return

    val_input1 = count_files_in_directory(source_dir + "/validation/Input_1")
    val_input2 = count_files_in_directory(source_dir + "/validation/Input_2")
    val_output = count_files_in_directory(source_dir + "/validation/Output")

    if not (val_input1 == val_input2 == val_output):
        return
    
    # Create a dictionary to map the old image numbers to the new image numbers
    for data_group in ["training", "validation"]: # Do this for both groups of data
        
        if data_group == "training":
            shuffled_training_nums = list(range(1, training_input1 + 1))
        else:
            shuffled_training_nums = list(range(1, val_input1 + 1))
        
        # Shuffle the numbers and making the old to new mapping
        random.shuffle(shuffled_training_nums)
        shuffled_trianing_map = {}

        for i in range(len(shuffled_training_nums)):
            shuffled_trianing_map[i + 1] = shuffled_training_nums[i]

        for root, dirs, files in os.walk(source_dir + f"/{data_group}/"):
            for filename in tqdm(files):

                new_folder_path = root.replace(source_dir, dest_dir)
                if not os.path.exists(new_folder_path): os.makedirs(new_folder_path)

                file_path = root + "/" + filename

                # Get old image numbers
                match = re.search(r'\d+', filename)
                number = int(match.group())
                new_number = shuffled_trianing_map[number]

                new_file_path = new_folder_path + "/" + filename.replace(str(number), str(new_number))

                shutil.copyfile(file_path, new_file_path)

    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)

    return

# If Main Declaration
if __name__ == "__main__":


    source_path = "./training_data/raw_data"
    dest_path = "./training_data/filtered_data"
    
    copy_and_rename_pictures(source_path, dest_path + "_temp")
    shuffle_data(dest_path + "_temp", dest_path)
    pad_images_parallel(dest_path)
