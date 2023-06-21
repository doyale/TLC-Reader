import cv2
import numpy as np
from scipy.signal import find_peaks, savgol_filter

def greyscale_lane(pixels, invert):
    greyscale_pixels = []
    for pixel in range(len(pixels)):
        #greyscale_pixel = int((pixels[pixel][0]/3 + pixels[pixel][1]/3 + pixels[pixel][2]/3))
        greyscale_pixel = int(pixels[pixel][1])
        if invert is True:
            greyscale_pixel = abs(greyscale_pixel-255)
        greyscale_pixels.append(int(greyscale_pixel))
    average = np.average(greyscale_pixels)
    #print(average)
    return greyscale_pixels, average

def get_pixel_line(image, start_x, start_y, end_x, end_y):
    len_x = abs(end_x-start_x)
    len_y = abs(start_y-end_y)
    factor = len_x/len_y
    total_len = np.sqrt(len_x**2+len_y**2)
    pixels = []
    positions = []
    y = min(start_y, end_y)
    x = min(start_x, end_x)
    # print(int(min(start_x, end_x)))
    # print(int(min(start_y, end_y)))
    # print(len_y)
    # print(range(len_y))
    for i in range(len_y):
        pixel = image[int(y+i), int(x+(i*factor))]
        # print(int(start_x+(i*factor))," ", int(end_y+i))
        # print(pixel)
        rel_len = np.sqrt(i**2 + (i * factor)**2)
        inv_rf = rel_len / total_len
        rf = abs(inv_rf - 1)
        pixels.append(list(pixel))
        if start_x > end_x:
            positions.append((int(min(start_y, end_y)+i), int(min(start_x, end_x)+(i*factor)), rf))
            #print(str(int(min(start_y, end_y)+i)), ", ", str(int(min(start_x, end_x)+(i*factor))))
            #print("case 1")
        else:
            positions.append((int(min(start_y, end_y)+i), int(end_x-(i*factor)), rf))
            #print("case 2")
        
        # print(len_y-i)
    print(positions)
    return pixels, positions

def resize_image(image, set_height):
    width = int(image.shape[1])
    height = int(image.shape[0])
    factor = set_height / height
    image = cv2.resize(image, [int(width*factor), int(height*factor)])
    set_width = width*factor
    return image, set_height, set_width

def autodetect_spots(pixel_lane, min_height = 60):
    pixel_array = np.array(pixel_lane)
    maxima = find_peaks(pixel_array, width=10, prominence=(2, None), height=min_height)
    return list(maxima[0])

def smooth_list(data, kernel_size = 50):
    data_convolved = savgol_filter(data, polyorder=3, window_length=kernel_size)
    return list(data_convolved)

def subtract_background(reference_values, values, positions):
    adjusted_values = []
    for i in range(len(values)):
        if positions[0][0] < positions[len(positions)-1][0]:
            #print(values[i], reference_values[positions[i][0]])
            adjusted_values.append(values[i]-reference_values[positions[i][0]])
        else:
            adjusted_values.append(values[i]-reference_values[positions[len(positions)-i][0]])
    average = np.average(adjusted_values)
    return adjusted_values, average