import tensorflow as tf
from PIL import Image
from tqdm import tqdm
import os
import cv2
import numpy as np

# Global Variable Definations
MAX_WIDTH = 1400
MAX_LENGTH = 2048

# Function Definations
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size

def pad_image(image_path, target_size):
    # Open the image
    image = Image.open(image_path)

    # Get the current size
    width, height = image.size

    # TODO: if width and height is too large


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

def pad_images(directory):
    for root, dirs, files in os.walk(directory):
        for filename in tqdm(files):
            target_size = (MAX_WIDTH, MAX_LENGTH)
            path = os.path.join(root, filename)
            pad_image(path, target_size)

def test_model(model_path, input_dir, output_dir):

    bw_images = []
    color_images = []
    initial_image = False
    for root, dirs, files in os.walk(input_dir):
        for filename in tqdm(files):
            file_path = f"{root}/{filename}"
            if initial_image:
                color_img = cv2.imread(file_path, cv2.IMREAD_COLOR)
                initial_image = False
                continue
            else:
                bw_img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                bw_img = np.expand_dims(bw_img, axis=-1)  # Add channel dimension
            bw_img = bw_img / 255.0
            bw_images.append(bw_img)
            color_images.append(color_img)
        initial_image = True

    bw_images = np.array(bw_images)
    color_images = np.array(color_images)
    model = tf.keras.models.load_model(model_path)

        
    with tf.device('/GPU:0'):
        results = model.predict([bw_images, color_images])

    file_number = 1
    for result in results[0]:
        rescaled_result = (result * 255).astype(np.uint8)

        # Convert the array to a PIL Image object
        output_image = Image.fromarray(rescaled_result)

        # Save the image as a file
        output_image.save(f"{output_dir}/Image_{file_number}.png")
        file_number += 1
    
    return


if __name__ == "__main__":
    
    model_path = "./models/model_20230815-093511.keras"
    input_dir = "./testing_data/Input"
    output_dir = "./Output"
    
    #pad_images(test_dir)
    test_model(model_path, input_dir, output_dir)
    