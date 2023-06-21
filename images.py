import skimage.io as io
from image_util import load_image, adjust_image, binary_image, blob_detection, plot_blobs

images = ["LS-2313V1R PE-EE 9-1 24 h +0,3 ml Bn ether.jpg", "LS-2310V1C. PE-EE 9-1.jpg", "LS-2310V3C PE-EE 9-1.jpg", "LS-2220V3-Säule F9-F18 DCM-MeOH 97-3.jpg", "LS-2310V2C PE-EE 9-1.jpg"]

for i in range(len(images)):
    loaded_image_path = images[i]
    loaded_image = load_image(loaded_image_path)
    loaded_image = adjust_image(loaded_image, 1, 5)
    #loaded_image = exposure.equalize_hist(loaded_image)
    io.imshow(binary_image(loaded_image, 100, True))
    io.show()
    plot_blobs(blob_detection(loaded_image, 60, 120, 20)).imshow(loaded_image, cmap = "gray")
    io.show()