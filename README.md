# PNG-JPG-to-WEBP-converter



This is a Python project primarily built for streamlining my own workflow but others are welcome to use it to do the same. Uses tkinter for UI and Pillow library for image conversion/compression.
The current capabilities are:
  * PNG and JPG to WEBP conversion and compression
  * WEBP compression (without conversion)

Process description and tips for use:

  PNG and JPG to WEBP conversion and compression:
    * Either choose the files via the "Choose Images" button or drag and drop files into the large white box.
    * Drag and drop will accept both files and folders, but the Choose File button should be used for individual images and Choose Folder for entire folders.
    * Converting a folder will result in all applicable files being located and populated in the list ([".png", ".jpg", ".jpeg", ".webp"])
    * Quality is able to be set from 0-100. Lower quality means a smaller image but worse quality. 
    * Pressing lossless will only convert to webp and not compress significantly depending on the image. 
    * No output folder is chosen by default. One must be selected via the Choose... button. 
    * Can handle large file amounts (No upper bound tested though).
    * Once all images are in the list, press convert and they will be in the output destination selected.
    * If you want to clear all images from the list press Clear Files, otherwise you can right click them individually to delete. 

  WEBP compression:
    * If an image is already a .webp file, you can drag and drop or bring it into the program, and it will only compress based on your quality selection. 
    * Same process applies.

More features/better UI may be added in the future. 
