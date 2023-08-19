# Imported Python Libraries
from PIL import Image
import random
import os

# Imported Third Party Libraries
import plotly.graph_objects as go
import matplotlib.pyplot as plt

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

    # Wait until a button is pressed or the window is closed
    plt.waitforbuttonpress()

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

# If Main Declaration
if __name__ == "__main__":

    dest_path = "./training_data/filtered_data"
    #create_image_dimensions_histogram(dest_path)
    display_random_images(dest_path + "/training/")