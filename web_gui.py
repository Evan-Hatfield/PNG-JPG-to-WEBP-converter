import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
import pathlib, concurrent.futures
from PIL import Image, features

# files user selects to be converted
selected_files = []
# all compatibable file types currently
file_types = [".png", ".jpg", ".jpeg", ".webp"]

# Function is called during actual image conversion
# - Effort (how much it is compressed) defaulted to 3 for simplicity and balance
# - Opens image and removes the meta data for better compression (Possible to keep meta data by setting to false)
# - Uses Pillow to convert image with given file name, either lossless or lossy depending on user selection

def to_webp_pillow(inimg_path, out_dir, quality, lossless=False, strip=True):
    effort = 3  # effort hard coded to 3 for balance
    inimg_path = pathlib.Path(inimg_path)
    out = pathlib.Path(out_dir) / (inimg_path.stem + ".webp")

    with Image.open(inimg_path) as image:

        # remove metadeta if present for greater compression
        if strip:
            image.info.pop("exif", None)

        if lossless:
            image.save(out, format="WEBP", lossless=True, method=effort)
        else:
            image.save(out, format="WEBP", quality=quality, method=effort)

    return out

# Function called when user clicks Choose images button
# - Shows all files from file_type array in explorer
# - Adds to selected files list for every file selected

def pick_files():
    files = filedialog.askopenfilenames(filetypes=[("Images", file_types)])
    if not files:
        return
    for f in files:
        if f not in selected_files:
            selected_files.append(f)
            file_list.insert("end", f)

# Function called when user clicks Choose Folder button
# - Shows only folders in explorer
# - Uses rglob function to recursively find all file types within the file_types,
# then appends all file paths to the image_paths list
# - If nothing found, return with error
# - Otherwise, add files to the list via add_files method
 
def pick_folder():
    folder = filedialog.askdirectory(title="Select Folder Containing Images")
    if not folder:
        return

    image_paths = []
    for path in pathlib.Path(folder).rglob("*"):
        if path.suffix.lower() in file_types:
            image_paths.append(str(path))

    if not image_paths:
        messagebox.showinfo("No Images Found", "No PNG or JPG files found in that folder.")
        return

    add_files(image_paths)

# Function called when user clicks Clear Files button
# - All files cleared in list
# - If no files exist, warning sent

def clear_files():
    if selected_files:
        selected_files.clear()
        file_list.delete(0, "end")
        messagebox.showinfo("Files Cleared", "All files have been removed.")
    else:
        messagebox.showwarning("No Files", "There are no files to clear.")

# Function called when Choose... button is selected. 
# - Takes directory information from user selection

def pick_out_dir():
    path = filedialog.askdirectory(title="Choose Output Folder")
    if path: 
        out_var.set(path)

# Function called files added via drag and drop option. 
# - Images are added with case insensitivity and only if the image is not already queued to be converted
# - File types are limited to .png, .jpg and .jpeg extensions

def add_files(paths):
    for p in paths:
        if pathlib.Path(p).suffix.lower() in file_types and p not in selected_files:
            selected_files.append(p)
            file_list.insert("end", p)

# Function called when either a file or a folder is drag and dropped
# - If path is a file, it will check against file_types, and if match is found, it
# adds to list of files to be displayed in the box
# - If path is a folder, it is added to list of folders to be added.
# - Finally, all folders are parsed recursively for files within file_types, 
# and all files that match are added to the list to be converted
# - All paths are converted to strings and added to list

def on_drop(event):
    paths = root.splitlist(event.data)
    folders = []
    files = []
    string_paths = []

    for p in paths:
        path = pathlib.Path(p)
        if path.is_dir():
            folders.append(path)
        elif path.suffix.lower() in file_types:
            files.append(path)

    for folder in folders:
        for f in folder.rglob("*"):
            if f.suffix.lower() in file_types:
                files.append(f)

    for f in files:
        string_paths.append(str(f))

    add_files(string_paths)

# Helper Function called when user deletes files individually in list
# - Path for file under cursor select is returned

def get_selected_path():
    selected_path = []
    for index in file_list.curselection():
        selected_path.append(file_list.get(index))
    return selected_path

# Function called when user deletes files individually in list
# - If no selection available, return error
# - Otherwise, remove files from list if possible via path

def remove_selected():
    paths = get_selected_path()
    if not paths:
        messagebox.showwarning("No Selection", "Select one or more items first.")
        return

    for p in paths:
        try:
            selected_files.remove(p)
        except ValueError:
            pass

    file_list.delete(0, "end")
    for f in selected_files:
        file_list.insert("end", f)

# Function called when event occurs (Right mouse click)
# - Shows right click menu (Currently only removal option)

def show_context_menu(event):
    try:
        index = file_list.nearest(event.y)
        if index >= 0:
            if index not in file_list.curselection():
                file_list.selection_clear(0, "end")
                file_list.selection_set(index)
                file_list.activate(index)
    except Exception:
        pass
    ctx.tk_popup(event.x_root, event.y_root)

# Function called when convert button pressed. 
# - Collects all selected image paths
# - Ensures Pillow has WebP support on user computer.
# - Calls to_webp_pillow for each conversion during a multithreading process.
# - Creates future objects as placeholders for the eventual compressed image in the destination folder
# - All successful/unsuccessful conversions are tracked and information on errors is displayed at end of conversion

def convert():
    # If list exists, grab list, otherwise grab the single file if it exists
    paths_strs = []
    if selected_files:
        paths_strs = selected_files
    elif file_var.get().strip():
        paths_strs = [p for p in file_var.get().splitlines() if p.strip()]

    if not paths_strs:
        return messagebox.showwarning("No files", "Select images first.")

    paths = [pathlib.Path(p) for p in paths_strs]

    # Resolve output dir and ensure it exists
    out = pathlib.Path(out_var.get()).expanduser().resolve()
    if not out.exists():
        return messagebox.showerror("Invalid Folder", "The selected output folder no longer exists.")


    # Verify Pillow has WebP support
    if not features.check('webp'):
        return messagebox.showerror(
            "WebP not supported", "Hopefully this error doesn't come up"
        )

    # Reading UI information for conversion
    try:
        quality = int(quality_var.get())
    except Exception:
        quality = 80 # default 80 if nothing is entered
    lossless = bool(lossless_var.get())

    successful_conversions = 0
    failed_conversions = 0
    errors = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_images = {}
        for p in paths:
            future_image = executor.submit(to_webp_pillow, p, out, quality, lossless, True)
            future_images[future_image] = p 
        for future_image, src in future_images.items():
            try:
                destination = future_image.result() 
                if destination and destination.exists():
                    successful_conversions += 1
                else:
                    failed_conversions += 1
                    errors.append(f"{src.name}: output missing")
            except Exception as e:
                failed_conversions += 1
                errors.append(f"{src.name}: {e}")

    if failed_conversions == 0 and successful_conversions > 0:
        messagebox.showinfo("Done", f"Converted {successful_conversions} file(s) → {out}")
    elif successful_conversions > 0:
        messagebox.showwarning("Partial success",
                               f"{successful_conversions} converted, {failed_conversions} failed.\nOutput: {out}\n\nErrors:\n" + "\n".join(errors[:10]))
    else:
        messagebox.showerror("All failed",
                             "No files were converted.\n\nErrors:\n" + "\n".join(errors[:15]))


# Set up UI
root = TkinterDnD.Tk()
root.title("Convert JPG/PNG to Webp")
root.geometry("600x500")

# Frame for choose image and clear image buttons to set up side by side
btn_frame = tk.Frame(root)
btn_frame.pack(fill="x", padx=10, pady=6)
tk.Label(root, text="Selected Images (drag images directly or click option above):", fg="gray").pack(anchor="n", padx=50)

tk.Button(btn_frame, text="Choose Images", command=pick_files).pack(side="left", expand=True, fill="x", padx=(0, 5))
file_var = tk.StringVar()
tk.Message(root, textvariable=file_var, width=500).pack(fill="both", padx=10)

file_list = tk.Listbox(root, selectmode="extended")
file_list.pack(fill="both", expand=True, padx=10, pady=(0,10))

file_list.drop_target_register(DND_FILES)
file_list.dnd_bind("<<Drop>>", on_drop)

tk.Button(btn_frame, text="Clear Files", command=clear_files).pack(side="left", expand=True, fill="x", padx=(5, 0))
tk.Button(btn_frame, text="Choose Folder", command=pick_folder).pack(side="left", expand=True, fill="x", padx=(5, 5))

ctx = tk.Menu(root, tearoff=0)
ctx.add_command(label="Remove Selected", command=remove_selected)

# Binds for windows
file_list.bind("<Button-3>", show_context_menu)
# Binds for mac
file_list.bind("<Control-Button-1>", show_context_menu)
file_list.bind("<Button-2>", show_context_menu)

# Frame for quality and lossless selection to be side by side
frm = tk.Frame(root)
frm.pack(fill="x", padx=10, pady=6)

tk.Label(frm, text="Quality (0-100):").grid(row=0, column=0, sticky="w")
quality_var = tk.StringVar(value="80")
tk.Entry(frm, textvariable=quality_var, width=5).grid(row=0, column=1, sticky="w")

lossless_var = tk.BooleanVar(value=False)
tk.Checkbutton(frm, text="Lossless", variable=lossless_var).grid(row=0, column=2, sticky="w")

# Frame for output selection bar and button, with conversion button below
tk.Label(root, text="Output folder:").pack(anchor="w", padx=10)
row = tk.Frame(root)
row.pack(fill="x", padx=10)
out_var = tk.StringVar(value="")
tk.Entry(row, textvariable=out_var).pack(side="left", fill="x", expand=True)
tk.Button(row, text="Choose…", command=pick_out_dir).pack(side="left", padx=8)

tk.Button(root, text="Convert", command=convert).pack(padx=10, pady=10)

root.mainloop()