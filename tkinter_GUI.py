from tkinter import *
import cv2
import copy
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter.filedialog as dialog
import util

##DEBUG VAR
global debug
debug = True


## GLOBAL VARS

global click_x
global click_y
global drag_x
global drag_y
global release_x
global release_y
global line
global im_height
global im_width
global cv2_image
global cv2_backup_image
global reference
global reference_values
reference = False
reference_values = []


## FUNCTIONS

def cv2_to_tkinter(image, height: int):
    """
    Function for converting cv2 bgr images into tkinter-readable rgb images.
    Rescales the image to the selected height.

    ---INPUT---
    - image: the cv2 bgr image to be converted
    - height: the desired height to be scaled to

    ---OUTPUT---
    - imgtk: The tkinter readable rgb image.
    - im_height: The height of the scaled image (should be equal to the input "height").
    - im_width: The width of the scaled image.
    """
    global debug
    image, im_height, im_width = util.resize_image(image, height)
    b, g, r = cv2.split(image)
    image = cv2.merge((r, g, b))
    im = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(im)

    if debug == True:
        print("Image converted to tkinter format, resized to height = " + str(im_height) + " px, width = " + str(int(im_width)) + "px")

    return imgtk, im_height, im_width


def x_y_click(event):
    global click_x, click_y, debug
    click_x, click_y = event.x, event.y

    if debug == True:
        print("Click registered at x = " + str(event.x) + ", y = " + str(event.y))
    

def x_y_drag(event):
    global click_x, click_y, drag_x, drag_y, line
    if event.x >= 0 and event.y >= 0 and event.x <= im_width and event.y <= im_height:
        drag_x, drag_y = event.x, event.y
        image_canvas.delete(line)
        line = image_canvas.create_line(click_x, click_y, drag_x, drag_y, fill="blue", width=5)

        if debug == True:
            print("Drag registered at x = " + str(event.x) + ", y = " + str(event.y))

def x_y_release(event):
    global click_x, click_y, release_x, release_y, cv2_image, cv2_backup_image, line, reference, reference_values
    release_x, release_y = event.x, event.y
    if reference is False or reference is None:
        line = image_canvas.create_line(click_x, 0, click_x, im_height, fill="red", width=5)
        pixels = []
        positions = []
        for y in range(im_height-1):
            positions.append([release_x, y])
            pixels.append(list(cv2_image[y, release_x]))
        reference_values, _ = util.greyscale_lane(pixels, False)
        reference = True
    else:
        cv2_backup_image = copy.deepcopy(cv2_image)
        pixels, positions = util.get_pixel_line(cv2_backup_image, click_x, click_y,release_x, release_y)
        grey_pixels, average = util.greyscale_lane(pixels, False)
        plt.plot(grey_pixels, label="data")
        grey_pixels_corr, bg_average = util.subtract_background(reference_values, grey_pixels, positions)
        grey_pixels_corr = util.smooth_list(grey_pixels_corr, 35)
        plt.plot(grey_pixels_corr, label="data-bg", linewidth=3.0)
        plt.plot(reference_values, label="background")
        plt.legend()
        corr_height = (average-bg_average)*0.5
        maxima = util.autodetect_spots(grey_pixels_corr, corr_height)
        cv2_backup_image, _, _ = util.resize_image(cv2_backup_image, 600)
        for i in range(len(maxima)):
            # print(maxima[i], ", ", int(grey_pixels_corr[maxima[i]]))
            plt.annotate("X", xy=(maxima[i]-4, grey_pixels_corr[maxima[i]]-1), weight="bold")
            cv2.circle(cv2_backup_image, (positions[maxima[i]][1], positions[maxima[i]][0]), 6, (100, 100, 255), 2, lineType=cv2.LINE_AA)
            cv2.putText(img=cv2_backup_image, text=str(positions[maxima[i]][2])[:4], org=(positions[maxima[i]][1]+12, positions[maxima[i]][0]+6), 
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, lineType=cv2.LINE_AA, color=(255, 255, 255), thickness=1)
        plt.annotate(">", xy=(0, corr_height), weight="bold")
        plt.show()
        # debug code (2 lines)
        # filename = str(dialog.askopenfilename())
        # cv2_backup_image = cv2.imread(filename, 1)
        image, _, _ = cv2_to_tkinter(cv2_backup_image, 600)
        image_canvas.delete("TLC-image")
        cv2.imshow("Image", cv2_backup_image)
        image_canvas.grid(row=1, column=0, rowspan=5)
        image_canvas.create_image(0, 0, image=image, anchor="nw", tag="TLC-image")
        print("test")

    if debug == True:
        print("Release registered at x = " + str(event.x) + ", y = " + str(event.y))

# initialization stuff
root = Tk()
root.title("TLC Interpreter")
root.iconbitmap("icon.ico")


# test code
filename = str(dialog.askopenfilename())
cv2_image = cv2.imread(filename, 1)

image, im_height, im_width = cv2_to_tkinter(cv2_image, 600)


# definitions of all components
image_label = Label(root, text="TLC Image")
image_canvas = Canvas(root, bg="black", width=im_width, height=im_height)
line = image_canvas.create_line(0,0,0,1, fill="blue", width=0)
graph_label = Label(root, text="Intensity Graphs")


# position sof all components
image_label.grid(row=0, column=0)
image_canvas.grid(row=1, column=0, rowspan=5)
graph_label.grid(row=0, column=1, columnspan=2)


# additional code
image_canvas.create_image(0, 0, image=image, anchor="nw", tag="TLC-image")
image_canvas.bind("<Button-1>", x_y_click)
image_canvas.bind("<B1-Motion>", x_y_drag)
image_canvas.bind("<ButtonRelease-1>", x_y_release)


# main loop
root.mainloop()