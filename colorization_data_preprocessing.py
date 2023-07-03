# Imported Python Libraries
import os
from PIL import Image


# Imported Third Party Libraries
import plotly.graph_objects as go

# Global Variable Definations


# Function Definations
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size

def create_image_dimensions_histogram(directory):

    image_counter = 0
    dimensions = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, filename)
                image_dimensions = get_image_dimensions(image_path)
                
                image_counter += 1
                if ((image_dimensions[0] < 1400) and (image_dimensions[1] < 1900)):
                    dimensions.append(image_dimensions)

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



# If Main Declaration
if __name__ == "__main__":
    
    directory_path = "E:/ml_color_data/training_data/raw_data"
    create_image_dimensions_histogram(directory_path)