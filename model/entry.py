"""
import cv2
from tensorflow import keras
import numpy as np
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'ResNet18_hue_2_at_30.keras')
model = keras.models.load_model(filename)

def predict(img):
    image = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    averageing_kernel = np.ones((7,7))*(1/49)
    gaussian = np.array([[1,2,1],[2,4,2],[1,2,1]])*(1/16)

    convolution_kernel = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    convolution_top = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])

    result = cv2.filter2D(image, -1, averageing_kernel)
    left = cv2.filter2D(result, -1, convolution_kernel)
    top = cv2.filter2D(result, -1, convolution_top)
    gaus = cv2.filter2D((top+left)/2, -1, gaussian)

    gaus = cv2.filter2D(image, -1, convolution_kernel)
    gaus = cv2.filter2D(gaus, -1, averageing_kernel)
    gaus = cv2.filter2D(gaus, -1, averageing_kernel)

    offset = 10

    desired_height = int(img.height/offset)-(int(80/offset))
    desired_width = int(img.width/offset)-(int(80/offset))

    xloc = []
    yloc = []
    for i in range(desired_height):
        for j in range(desired_width):
            if(gaus[i*offset:i*offset+80,j*offset:j*offset+80].max() > 60):
                xloc.append(i)
                yloc.append(j)


    a = np.zeros((desired_height, desired_width))

    for i in range(len(xloc)):
        cropped = img.crop((yloc[i]*offset, xloc[i]*offset, yloc[i]*offset + 80, xloc[i]*offset + 80))
        arr = np.array(cropped)
        x = np.expand_dims(arr, axis=0)
        yhat = model.predict(x, verbose = 0)
        a[xloc[i]][yloc[i]] = yhat
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
    return(b.max() - 1)
"""
def predict(img):
    return 1