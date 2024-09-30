import os
import tkinter as tk
from tkinter import filedialog, messagebox

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer App")
        self.root.geometry("800x600")

        # Create frames
        self.frame_left = tk.Frame(self.root, width=200, height=600, bg="gray")
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_right = tk.Frame(self.root, width=600, height=600, bg="white")
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create treeview
        self.treeview = tk.ttk.Treeview(self.frame_left)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Create buttons
        self.button_new_folder = tk.Button(self.frame_left, text="New Folder", command=self.create_new_folder)
        self.button_new_folder.pack(fill=tk.X)

        self.button_delete = tk.Button(self.frame_left, text="Delete", command=self.delete_file_or_folder)
        self.button_delete.pack(fill=tk.X)

        self.button_rename = tk.Button(self.frame_left, text="Rename", command=self.rename_file_or_folder)
        self.button_rename.pack(fill=tk.X)

        # Create listbox
        self.listbox = tk.Listbox(self.frame_right, width=60, height=30)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Initialize treeview
        self.treeview.heading("#0", text="File System")
        self.treeview.insert("", "end", "root", text="Root", open=True)
        self.populate_treeview("root", "/")

    def populate_treeview(self, parent, path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                self.treeview.insert(parent, "end", item, text=item, open=True)
                self.populate_treeview(item, item_path)
            else:
                self.treeview.insert(parent, "end", item, text=item)

    def create_new_folder(self):
        folder_name = filedialog.askdirectory()
        if folder_name:
            os.mkdir(folder_name)
            self.treeview.insert("root", "end", folder_name, text=os.path.basename(folder_name), open=True)

    def delete_file_or_folder(self):
        selected_item = self.treeview.selection()[0]
        item_path = os.path.join(self.treeview.parent(selected_item), self.treeview.item(selected_item, "text"))
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            os.rmdir(item_path)
        self.treeview.delete(selected_item)

    def rename_file_or_folder(self):
        selected_item = self.treeview.selection()[0]
        item_path = os.path.join(self.treeview.parent(selected_item), self.treeview.item(selected_item, "text"))
        new_name = filedialog.askstring("Rename", "Enter new name", initialvalue=self.treeview.item(selected_item, "text"))
        if new_name:
            os.rename(item_path, os.path.join(os.path.dirname(item_path), new_name))
            self.treeview.item(selected_item, text=new_name)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    app.run()
