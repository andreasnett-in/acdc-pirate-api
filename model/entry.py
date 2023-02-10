from matplotlib import pyplot as plt
from tensorflow import keras
import numpy as np
import tensorflow as tf
import os
from PIL import Image
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'ResNet18_hue_2_at_30.keras')
model = keras.models.load_model(filename)

def predict(image):
    img = Image.fromarray(image)

    offset = 10

    desired_height = int(img.height/offset)-(int(80/offset))
    desired_width = int(img.width/offset)-(int(80/offset))

    a = np.zeros((desired_height, desired_width))

    for i in range(desired_height):
        for j in range(desired_width):
            cropped = img.crop((j*offset, i*offset, j*offset + 80, i*offset + 80))
            arr = np.array(cropped)
            x = np.expand_dims(arr, axis=0)
            yhat = model.predict(x, verbose = 0)
            a[i][j] = yhat

    b = np.zeros((desired_height, desired_width))

    index = 2

    for i in range(desired_height):
        for j in range(desired_width):
            if(a[i][j] < 0.5):
                b[i][j] = 1
            else:
                for ii in range(3):
                    for jj in range(3):
                        if (b[i+ii-1][j+jj-1] > 1):
                            b[i][j] = b[i+ii-1][j+jj-1]
                if(b[i][j] == 0):
                    b[i][j] = index
                    index = index + 1
    return (b.max() - 1)


