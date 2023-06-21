import cv2
from cv2 import *
import tkinter.messagebox as mb
import copy
import util

img_click_x = 0
img_click_y = 0
new_circle = False
new_lane = False
cached_image = None
image_height = 800

def spot_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global img_click_y
        global img_click_x
        global new_circle
        img_click_x = x
        img_click_y = y
        new_circle = True

def lanes_click(event, x, y, flags, params):
    global img_click_y
    global img_click_x
    global new_lane
    if event == cv2.EVENT_LBUTTONDOWN:
        img_click_x = x
        img_click_y = y
        new_lane = True

def lanes_release(event, x, y, flags, params):
    global img_click_y
    global img_click_x
    global new_lane
    if event == cv2.EVENT_LBUTTONUP:
        img_click_x = x
        img_click_y = y
        new_lane = True
    if event == cv2.EVENT_MOUSEMOVE:
        img_click_x = x
        img_click_y = y

def select_spots(loaded_image):
    global cached_image
    global image_height
    restart = True
    while restart == True:
        restart = False
        image = copy.deepcopy(loaded_image)
        spot_coords = []
        image = util.resize_image(image, image_height)
        exit = False
        while exit is False:
            global new_circle
            cv2.imshow("Image", image)
            cv2.setMouseCallback("Image", spot_click)
            key = cv2.waitKey(5)
            if new_circle is True:
                global img_click_y
                global img_click_x
                cached_image = copy.deepcopy(image)
                cv2.circle(image, (img_click_x, img_click_y), 6, (0, 0, 255), 2, lineType=cv2.LINE_AA,)
                #print("Circle drawn")
                new_circle = False
                changed_state = True
                spot_coords.append([img_click_x, img_click_y])
            if key == 27:
                #print("Exit prompt")
                exit = mb.askokcancel(title="Cancel spot selection?", message="Cancel spot selection?")
                if exit is True:
                    cv2.destroyAllWindows()
                    restart = mb.askyesno(title="Restart?", message="Restart selection?")
            elif key == 13:
                exit = mb.askokcancel(title="Finish spot selection?", message="Finish spot selection?")
            elif key == 8 and changed_state == True:
                #print(changed_state)
                image = copy.deepcopy(cached_image)
                changed_state = False
                cv2.imshow("Image", image)
                spot_coords.pop()
                #print("removed previous spot.")
            elif key != -1:
                print(chr(key), ", ", str(key))
    cv2.destroyAllWindows()
    return spot_coords, image

def select_lanes(loaded_image):
    global cached_image
    global new_lane
    global img_click_x
    global img_click_y
    changed_state = False
    restart = True
    while restart is True:
        restart = False
        exit = False
        lane_coords = []
        image = copy.deepcopy(loaded_image)
        while exit is False:
            cv2.imshow("Image", image)
            cv2.setMouseCallback("Image", lanes_click)
            key = cv2.waitKey(5)
            if new_lane is True and changed_state is False:
                changed_state = True
                new_lane = False
                start_x = img_click_x
                start_y = img_click_y
                cached_image = copy.deepcopy(image)
                cv2.circle(image, (start_x, start_y), 3, (255, 0, 0), 3, lineType=cv2.LINE_AA)
                image_preview = copy.deepcopy(image)
                while exit is False:
                    image = copy.deepcopy(image_preview)
                    cv2.line(image, (start_x, start_y), (img_click_x, img_click_y), (255, 0, 0), 2, lineType=cv2.LINE_AA)
                    cv2.imshow("Image", image)
                    cv2.setMouseCallback("Image", lanes_release)
                    key = cv2.waitKey(5)
                    if new_lane is True:
                        new_lane = False
                        end_x = img_click_x
                        end_y = img_click_y
                        cv2.circle(image, (end_x, end_y), 3, (255, 0, 0), 3, lineType=cv2.LINE_AA)
                        cv2.line(image, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2, lineType=cv2.LINE_AA)
                        lane_coords.append([start_x, start_y, end_x, end_y])
                        break
            elif key == 27:
                #print("Exit prompt")
                exit = mb.askokcancel(title="Cancel spot selection?", message="Cancel spot selection?")
                if exit is True:
                    cv2.destroyAllWindows()
                    restart = mb.askyesno(title="Restart?", message="Restart selection?")
            elif key == 13:
                exit = mb.askokcancel(title="Finish spot selection?", message="Finish spot selection?")
            elif key == 8 and changed_state is True:
                #print(changed_state)
                image = copy.deepcopy(cached_image)
                changed_state = False
                cv2.imshow("Image", image)
                lane_coords.pop()
                #print("removed previous spot.")
            elif key != -1:
                print(chr(key), ", ", str(key))
    cv2.destroyAllWindows()
    return lane_coords, image

def background(loaded_image):
    global image_height
    global cached_image
    global new_circle
    restart = True
    while restart == True:
        restart = False
        image = copy.deepcopy(loaded_image)
        image, _, _ = util.resize_image(image, image_height)
        exit = False
        selected = False
        while exit is False:
            cv2.imshow("Image", image)
            cv2.setMouseCallback("Image", spot_click)
            key = cv2.waitKey(5)
            if selected is False and new_circle is True:
                selected = True
                new_circle = False
                global img_click_x
                global img_click_y
                cached_image = copy.deepcopy(image)
                cv2.line(image, (img_click_x, 0), (img_click_x, 799), (50, 50, 255), 2, lineType=cv2.LINE_AA)
                changed_state = True
            if key == 27:
                #print("Exit prompt")
                exit = mb.askokcancel(title="Cancel reference selection?", message="Cancel reference selection?")
                if exit is True:
                    cv2.destroyAllWindows()
                    restart = mb.askyesno(title="Restart?", message="Restart selection?")
            elif key == 13:
                exit = mb.askokcancel(title="Finish reference selection?", message="Finish reference selection?")
            elif key == 8 and changed_state == True:
                #print(changed_state)
                image = copy.deepcopy(cached_image)
                changed_state = False
                cv2.imshow("Image", image)
                img_click_x = None
                img_click_y = None
                selected = False
                #print("removed previous spot.")
            elif key != -1:
                print(chr(key), ", ", str(key))
    cv2.destroyAllWindows()
    pixels = []
    positions = []
    for y in range(image_height-1):
        positions.append([img_click_x, y])
        pixels.append(list(loaded_image[y, img_click_x]))
    greyscale_pixels, _ = util.greyscale_lane(pixels, True)
    #print(greyscale_pixels, positions)
    return greyscale_pixels, positions