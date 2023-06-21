import cv2
import interactive
import util
import matplotlib.pyplot as plt
import copy
import tkinter.messagebox as mb
import tkinter.filedialog as dialog
import os
while True:
    #filename = input("File Path and Name: ")
    filename = str(dialog.askopenfilename())
    print(filename)
    image = cv2.imread(filename, 1)
    image, _, _ = util.resize_image(image, 800)
    reference_values, reference_positions = interactive.background(image)
    exit_pg = None
    while exit_pg is None:
        original_image = copy.deepcopy(image)
        plt.plot(reference_values, label="background")
        #print(reference_values, reference_positions)
        coords, image = interactive.select_lanes(image)
        if coords == []:
            break
        #print(coords)
        pixels, positions = util.get_pixel_line(original_image, coords[0][0], coords[0][1], coords[0][2], coords[0][3])
        #print(positions)
        grey_pixels, average = util.greyscale_lane(pixels, True)
        #print(grey_pixels)
        plt.plot(grey_pixels, label="data")
        grey_pixels_corr, bg_average = util.subtract_background(reference_values, grey_pixels, positions)
        grey_pixels_corr = util.smooth_list(grey_pixels_corr, 35)
        plt.plot(grey_pixels_corr, label="data-bg", linewidth=3.0)
        plt.legend()
        corr_height = (average-bg_average)*0.1
        if corr_height > 50:
            print("Average difference between background and smaple is high, is the TLC plate overloaded?")
        maxima = util.autodetect_spots(grey_pixels_corr, corr_height)
        # print(positions)
        backup_image = copy.deepcopy(image)
        for i in range(len(maxima)):
            # print(maxima[i], ", ", int(grey_pixels_corr[maxima[i]]))
            plt.annotate("X", xy=(maxima[i]-4, grey_pixels_corr[maxima[i]]-1), weight="bold")
            cv2.circle(backup_image, (positions[maxima[i]][1], positions[maxima[i]][0]), 6, (100, 100, 255), 2, lineType=cv2.LINE_AA)
            cv2.putText(img=backup_image, text=str(positions[maxima[i]][2])[:4], org=(positions[maxima[i]][1]+12, positions[maxima[i]][0]+6), 
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, lineType=cv2.LINE_AA, color=(255, 255, 255), thickness=1)
        plt.annotate(">", xy=(0, corr_height), weight="bold")
        plt.show()
        while exit_pg is None:
            cv2.imshow("Image", backup_image)
            key = cv2.waitKey(20)
            if key == 13 or key == 27:
                if mb.askyesno(title="Add another lane?", message="Do you want to add another lane?") is True:
                    image = copy.deepcopy(backup_image)
                    exit_pg = None
                    break
                else:
                    exit_pg = mb.askyesnocancel(title="Save image?", message="Save image before quitting?")
                    if exit_pg is True:
                        filepath = str(dialog.askdirectory())
                        print("File saved successfully as " + filepath + "/" + os.path.basename(filename)[:len(filename)-4] + "_modified.png" + "?: ", cv2.imwrite(filepath + "/" + os.path.basename(filename)[:len(filename)-4] + "_modified.png", backup_image))
        # print("showed image")
    if mb.askyesno(title="Process another TLC?", message="Do you want to process another TLC?") is True:
        cv2.destroyAllWindows()
    else:
        cv2.destroyAllWindows()
        break
        #coords, image = interactive.select_spots(image)
        #print(coords)
        # if input("add lane? (Y/n): ") == "n":
        #     break