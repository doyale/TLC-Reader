# TLC-Reader
Barebones implementation which reads RF values form TLC plates

# How to use
- When launching the program, a file dialog will open. Select the image file you wish to process
- The image will open. Click anywhere on the image to select a representative background sample (make sure that none of the TLC spots are on the resulting red line). If you aren't happy with the selected column, you may undo your choice using backspace.
- Press enter and confirm your choice by clicking "Yes" in the popup. The image will now re-open.
- Click on the rightmost baseline position which you wish to process and drag the cursor towards the solvent front, making sure to slant the line at such an angle that all spots are covered. You can also undo this selection by pressing backspace.
- If you have the debug version of the program, a graph window containing the raw data will pop up. The program will proceed once this window is closed.
- The original image, modified with the detected spots and respective RF-values will be shown. Press enter to continue.
- A popup box will prompt you to add another lane. If you click "Yes" the lane selection process can be repeated with the next rightmost lane. If you click "No", you will be prompted to save the image.
- If you initiate the save procedure, a file dialog will pop up. select the folder you want to save the resulting image in. The image will be saved as <original_file_name>_modified.jpg 
- You can then process another TLC or quit the program.
- The Program can be closed at any time by pressing escape and confirming in the dialog box
