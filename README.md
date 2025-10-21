# PNG/JPG to WEBP Converter and Compressor

This is a Python project primarily built for streamlining my own workflow, but others are welcome to use it too.  
It uses **Tkinter** for the UI and **Pillow** for image conversion and compression.

---

## 🧰 Current Capabilities
- **PNG and JPG → WEBP conversion and compression**
- **WEBP compression (without conversion)**

---

## ⚙️ Process Description and Tips for Use

### PNG and JPG → WEBP Conversion and Compression
- Either choose the files via the **“Choose Images”** button or **drag and drop** files into the large white box.
- Drag and drop accepts both files and folders, but the *Choose File* button should be used for individual images, and *Choose Folder* for entire folders.
- Converting a folder will locate and populate all applicable files in the list (`.png`, `.jpg`, `.jpeg`, `.webp`).
- **Quality** can be set from 0–100. Lower quality means smaller file size but worse visual quality.
- Checking **Lossless** will preserve image data (little to no compression, depending on the source).
- **No output folder** is chosen by default — one must be selected via the **“Choose…”** button.
- Handles large file amounts (no upper bound tested yet).
- Once all images are in the list, press **Convert** and they’ll appear in the selected output destination.
- To clear all images from the list, press **Clear Files**. You can also right-click individual entries to delete them.

### WEBP Compression
- If an image is already a `.webp` file, you can drag and drop or load it via **Choose Images**.
- The image will be recompressed based on your selected quality setting.
- The same process and output folder rules apply.

---

## 🔮 Future Plans
More features and improved UI may be added in future versions.
