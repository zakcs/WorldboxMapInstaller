import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import sys

save_folder_path = ""

class WorldboxMapInstaller:

    def __init__(self, master):
        self.master = master
        self.save_folder_path = save_folder_path
        self.wbox_path = ""
        self.preview_path = ""
        self.save_slot = ""
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Worldbox Map Installer", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=(10, 20))

        tk.Label(self.master, text="Save Folder:").grid(row=1, column=0, sticky="w", padx=10)
        tk.Entry(self.master, width=50, state="readonly", textvariable=tk.StringVar(value=self.save_folder_path)).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.master, text="Select Folder", command=self.select_save_folder).grid(row=1, column=2, padx=10)

        tk.Label(self.master, text="map.wbox File:").grid(row=2, column=0, sticky="w", padx=10)
        tk.Entry(self.master, width=50, state="readonly", textvariable=tk.StringVar(value=self.wbox_path)).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.master, text="Select File", command=self.select_wbox_file).grid(row=2, column=2, padx=10)

        tk.Label(self.master, text="preview.png File:").grid(row=3, column=0, sticky="w", padx=10)
        tk.Entry(self.master, width=50, state="readonly", textvariable=tk.StringVar(value=self.preview_path)).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.master, text="Select File", command=self.select_preview_file).grid(row=3, column=2, padx=10)

        tk.Button(self.master, text="Save Map", command=self.save_map).grid(row=5, column=1, pady=(20, 10))

    def load_save_folder(self):
        save_folder_path = ""
        if os.path.isfile("save_folder.json"):
            with open("save_folder.json", "r") as f:
                save_folder_path = json.load(f)
        if not os.path.isdir(save_folder_path):
            save_folder_path = filedialog.askdirectory(title="Select Save Folder")
            with open("save_folder.json", "w") as f:
                json.dump(save_folder_path, f)
        return save_folder_path

    def select_save_folder(self):
        self.save_folder_path = filedialog.askdirectory(title="Select Save Folder")
        with open("save_folder.json", "w") as f:
            json.dump(self.save_folder_path, f)
        self.create_widgets()

    def select_wbox_file(self):
        self.wbox_path = filedialog.askopenfilename(title="Select map.wbox file", filetypes=(("Worldbox Map Files", "*.wbox"),))
        self.create_widgets()

    def select_preview_file(self):
        self.preview_path = filedialog.askopenfilename(title="Select preview.png file", filetypes=(("WorldboxPreview Files", "*.png"),))
        self.create_widgets()
    
    def save_map(self):
     self.save_slot = simpledialog.askstring(title="Save Slot", prompt="Enter the save slot (e.g. 13)")
     save_slot_folder = os.path.join(self.save_folder_path, f"save{self.save_slot}")
     if not os.path.isdir(save_slot_folder):
         os.makedirs(save_slot_folder)
     else:
         for file_name in os.listdir(save_slot_folder):
             file_path = os.path.join(save_slot_folder, file_name)
             try:
                 if os.path.isfile(file_path):
                     os.unlink(file_path)
             except Exception as e:
                 print(e)
     shutil.copy(self.wbox_path, os.path.join(save_slot_folder, "map.wbox"))
     shutil.copy(self.preview_path, os.path.join(save_slot_folder, "preview.png"))
     self.wbox_path = ""
     self.preview_path = ""
     self.save_slot = ""
     self.create_widgets()

root = tk.Tk()
root.title("Worldbox Map Installer")
root.wm_iconbitmap('myicon.ico')
WorldboxMapInstaller(root)
root.mainloop()