import skimage.io as io
import skimage.exposure as exposure
import skimage.feature as si_feature
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

def load_image(path: str, greyscale: bool = False):
    image = plt.imread(path)
    if greyscale == True:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def adjust_image(image, gamma: float = 0, log: float = 0, sig: float = 0):
    if gamma != 0:
        image = exposure.adjust_gamma(image, gamma)
    if log != 0:
        exposure.adjust_log(image, log)
    if sig != 0:
        exposure.adjust_sigmoid(image, sig)
    return image


def binary_image(image, threshold = 127, inverted: bool = False):
    white = 255
    black = 0
    if inverted == True:
        ret, final_conv = cv2.threshold(image, threshold, 255, 0)
        final_conv = 255 - final_conv
        return final_conv
    else:
        ret, final_conv = cv2.threshold(image, threshold, 255, 0)
        return final_conv

def detect_stain(image):
    print("Detecting used stain type...")
    average_color_row = np.average(image, axis=0)
    average_color = np.average(average_color_row, axis=0)
    print("Average color: " + str(average_color.astype(int)))
    fig, image = plt.subplots()
    image.add_patch(plt.Circle((0, 2), 3, color=average_color/255.0, fill=True))
    io.show()
        
    return average_color.astype(int), image

def blob_detection(image, thresh_min: int = 5, thresh_max: int = 120, thresh_step: int = 10):
    blobs_out = []
    for threshold in range(thresh_min, thresh_max, thresh_step):
        print("Iteration " + str((threshold-thresh_min)//thresh_step+1) + " of " + str((thresh_max-thresh_min)//thresh_step))
        bw_image = binary_image(image, threshold, True)
        blobs = si_feature.blob_log(bw_image, max_sigma=59, min_sigma = 20, num_sigma=4, threshold=0.01, threshold_rel = 0.7, overlap = 0.01)
        for blob in blobs:
            invalid_blob = False
            x, y, area = blob
            perim = area*np.sqrt(2)/6
            #perim = 5
            print(perim)
            #print(blobs_out[:0])
            if invalid_blob == False:
                for dia_x in range(int(x - perim*2), int(x + perim*2)):
                    #print("Evaluating at x-pos: " + str(dia_x))
                    if invalid_blob == False:
                        for dia_y in range(int(y - perim/2), int(y + perim/2)):
                            #print("Evaluating at y-pos: " + str(dia_y))
                            if dia_x in [lx[0] for lx in blobs_out[::]] or dia_y in [ly[1] for ly in blobs_out[::]]:
                                #print("Invalid blob detected at x: " + str(x) + ", y: " + str(y))
                                invalid_blob = True
                                break
            if invalid_blob == False:
                print("Blob at x: " + str(x) + ", y: " + str(y) + "is VALID")
                blobs_out.append([x, y, area])
                #print(blobs_out)
            #else:
                print("Blob at x: " + str(x) + ", y: " + str(y) + "is INVALID")
                #print(blobs_out)
    return blobs_out


def plot_blobs(blobs):
    fig, image = plt.subplots()
    for blob in blobs:
        y, x, area = blob
        image.add_patch(plt.Circle((x, y), area*np.sqrt(2), color='red', fill=False))
    return image

#debug code:
images = []
for filename in glob.glob("*.jpg"):
    images.append(filename)

for filename in glob.glob("F:\\OneDrive - bwedu\\1-Dokumente\\Master\\4. Semester\\Masterarbeit\\DC\\*.jpg"):
    images.append(filename)

for i in range(len(images)):
    loaded_image_path = images[i]
    loaded_image = load_image(loaded_image_path)
    detect_stain(load_image(loaded_image_path, True))
    loaded_image = adjust_image(loaded_image, 1, 5)
    #loaded_image = exposure.equalize_hist(loaded_image)
    io.imshow(binary_image(loaded_image, 100, True))

    io.show()
    plot_blobs(blob_detection(loaded_image, 60, 120, 20)).imshow(loaded_image, cmap = "gray")
    io.show()