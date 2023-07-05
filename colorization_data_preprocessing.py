# Imported Python Libraries
import os
from PIL import Image
import shutil
import random
import time


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
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, filename)
                image_dimensions = get_image_dimensions(image_path)
                
                image_counter += 1
                if ((image_dimensions[0] <= MAX_WIDTH) and (image_dimensions[1] <= MAX_LENGTH)):
                    dimensions.append(image_dimensions)
                else:
                    #if (filename.split(".")[0] == "01"):
                    print(f"{root + filename}: {image_dimensions}")

    print(image_counter)
    print(len(dimensions))
    print((len(dimensions)/image_counter) * 100)
    width, height = zip(*dimensions)

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


def copy_and_rename_pictures(source_dir, dest_dir, prefix="image_", start_index=1):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    input_1_dir = input_2_dir = output_dir = dest_dir

    output_dir += "/Output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    input_2_dir += "/Input_2"
    if os.path.exists(input_2_dir):
        shutil.rmtree(input_2_dir)

    os.makedirs(input_2_dir)

    input_1_dir += "/Input_1"
    if os.path.exists(input_1_dir):
        shutil.rmtree(input_1_dir)

    os.makedirs(input_1_dir)

    index = start_index
    for root, dirs, files in os.walk(source_dir):

        first_page = True
        first_page_path = ""

        for filename in tqdm(files):
            

            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                source_path = os.path.join(root, filename)
                image_dimensions = get_image_dimensions(source_path)
                if ((image_dimensions[0] <= MAX_WIDTH) and (image_dimensions[1] <= MAX_LENGTH)):
                    if first_page:
                        first_page_path = source_path

                        first_page = False
                        continue
                    else:
                        
                        dest_filename = f"{prefix}{index}{os.path.splitext(filename)[1]}"

                        output_path = os.path.join(output_dir, dest_filename)
                        input_2_path = os.path.join(input_2_dir, dest_filename)
                        input_1_path = os.path.join(input_1_dir, dest_filename)

                        shutil.copyfile(first_page_path, input_1_path)
                        shutil.copyfile(source_path, output_path)

                        with Image.open(source_path) as img:
                            input_2_image = img.convert("L")
                            input_2_image.save(input_2_path)
                        
                        index += 1

def display_images(image_paths):
    fig, axes = plt.subplots(1, 3, figsize=(10, 5))

    for i, path in enumerate(image_paths):
        image = Image.open(path)

        if i == 1:
            # Convert the second image to black and white
            image = image.convert('L')
            cmap = 'gray'
        else:
            cmap = None

        axes[i].imshow(image, cmap=cmap)
        axes[i].axis('off')

    fig.suptitle(f"{image_paths[0].split('/')[-1]}")
    plt.tight_layout()
    plt.show()
                    
def display_random_images(diretory):

    input_1_dir = input_2_dir = output_dir = diretory

    output_dir += "/Output/"
    input_2_dir += "/Input_2/"
    input_1_dir += "/Input_1/"


    output_files = [filename for filename in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, filename))]
    input_2_files = [filename for filename in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, filename))]
    input_1_files = [filename for filename in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, filename))]

    if not (len(output_files) == len(input_2_files) == len(input_1_files)):
        return

    # for i in range(100):
    #     random_file_number = random.randint(1, len(output_files))
    #     print(output_files[random_file_number], input_2_files[random_file_number], input_1_files[random_file_number])

    for _ in range(1000):
        random_file_number = random.randint(1, len(output_files))
        image_paths = [input_1_dir + input_1_files[random_file_number], input_2_dir + input_2_files[random_file_number], output_dir + output_files[random_file_number]]
        display_images(image_paths)

def pad_images(directory):
    for root, dirs, files in os.walk(directory):
        for filename in tqdm(files):
            target_size = (MAX_WIDTH, MAX_LENGTH)
            path = os.path.join(root, filename)
            pad_image(path, target_size)


# If Main Declaration
if __name__ == "__main__":
    
    source_path = "E:/ml_color_data/training_data/raw_data"
    dest_path = "E:/ml_color_data/training_data/filtered_data"
    
    create_image_dimensions_histogram(dest_path)
    #copy_and_rename_pictures(source_path, dest_path)
    #pad_images(dest_path)

    display_random_images(dest_path)