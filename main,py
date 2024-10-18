from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButtonText as MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import os
import importlib.util
from kivy.utils import platform
import shutil
import os

class ComplexFileManager:
    def __init__(self, exit_callback, select_callback):
        """
        Initialize the complex file manager wrapper to manage file browsing.
        """
        self.exit_callback = exit_callback  # Exit callback to close the file manager
        self.select_callback = select_callback  # Callback to handle path selection

        self.file_manager = None  # This will hold the MDFileManager instance

    def get_file_manager(self):
        """
        Check if the file manager is already initialized, and initialize it if not.
        """
        if not self.file_manager:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_callback,
                select_path=self.select_callback,
                preview=True
            )
        return self.file_manager

    def show(self, path):
        """
        Show the file manager at the specified path.
        Initializes the file manager if necessary.
        """
        self.get_file_manager()  # Ensure the file manager is created
        if not self.file_manager_open():
            self.file_manager.show(path)

    def close(self):
        """
        Close the file manager if it's currently open.
        """
        if self.file_manager_open():
            self.file_manager.close()

    def file_manager_open(self):
        """
        Check if the file manager is open by checking its internal state.
        """
        return self.file_manager is not None and self.file_manager._window_manager_open

    def refresh(self):
        """
        Refresh the file manager's view. Use this when changes are made to the file system.
        """
        if self.file_manager_open():
            self.file_manager.show(self.file_manager.current_path)

class FileOperations(MDBoxLayout):
    def __init__(self, file_manager, **kwargs):
        super(FileOperations, self).__init__(**kwargs)
        self.file_manager = file_manager
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        self.delete_button = MDRaisedButton(
            text="Delete",
            on_release=self.delete_file
        )
        self.add_widget(self.delete_button)

        self.rename_button = MDRaisedButton(
            text="Rename",
            on_release=self.rename_file
        )
        self.add_widget(self.rename_button)

    def delete_file(self, instance):
        selected_file = self.file_manager.selection
        if selected_file:
            dialog = MDDialog(
                title="Confirm Deletion",
                text=f"Are you sure you want to delete {selected_file}?",
                buttons=[
                    MDRaisedButton(text="CANCEL", on_release=lambda x: dialog.dismiss()),
                    MDRaisedButton(text="DELETE", on_release=self.confirm_delete)
                ]
            )
            dialog.open()
        else:
            print("No file selected.")

    def confirm_delete(self, instance):
        selected_file = self.file_manager.selection
        try:
            if os.path.isfile(selected_file):
                os.remove(selected_file)
            else:
                os.rmdir(selected_file)  # Consider using shutil.rmtree for directories
            print(f"Deleted: {selected_file}")
            self.file_manager.refresh()  # Refresh the file manager view
        except Exception as e:
            print(f"Error deleting file: {e}")

    def rename_file(self, instance):
        selected_file = self.file_manager.selection
        if selected_file:
            current_name = os.path.basename(selected_file)
            dialog = MDDialog(
                title="Rename File",
                type="custom",
                content_cls=TextInput(hint_text="New name", text=current_name),
                buttons=[
                    MDRaisedButton(text="CANCEL", on_release=lambda x: dialog.dismiss()),
                    MDRaisedButton(text="RENAME", on_release=lambda x: self.confirm_rename(dialog))
                ]
            )
            dialog.open()
        else:
            print("No file selected.")

    def confirm_rename(self, dialog):
        selected_file = self.file_manager.selection
        new_name = dialog.content_cls.text
        new_path = os.path.join(os.path.dirname(selected_file), new_name)
        try:
            os.rename(selected_file, new_path)
            print(f"Renamed: {selected_file} to {new_path}")
            self.file_manager.refresh()  # Refresh the file manager view
            dialog.dismiss()
        except Exception as e:
            print(f"Error renaming file: {e}")

class MainInterface(MDBoxLayout):
    def __init__(self, app_instance, **kwargs):
        super(MainInterface, self).__init__(**kwargs)
        self.app = app_instance
        self.orientation = 'horizontal'

        # Use ComplexFileManager to manage file manager instance
        self.file_manager = ComplexFileManager(
            exit_callback=self.exit_manager,
            select_callback=self.select_path
        )

        # File operations widget that interacts with the file manager
        self.file_operations = FileOperations(self.file_manager)

        # Add only the file operations widget since the file manager will be dynamically shown
        self.add_widget(self.file_operations)

    def exit_manager(self, *args):
        """Close the file manager if it's open."""
        self.file_manager.close()

    def select_path(self, path):
        """Handles the selection of a file or directory."""
        print(f"Selected: {path}")

    def show_file_manager(self, path):
        """Display the file manager."""
        self.file_manager.show(path)  # Display the file manager
import logging

class FileBrowserApp(MDApp):
    def __init__(self, **kwargs):
        super(FileBrowserApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.plugins = []

    def build(self):
        self.main_interface = MainInterface(self)
        self.load_plugins()
        return self.main_interface

    def load_plugins(self):
        plugin_dir = 'plugins'
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)

        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py'):
                plugin_path = os.path.join(plugin_dir, filename)
                try:
                    plugin_name = filename[:-3]
                    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, 'Plugin'):
                        plugin = module.Plugin(app=self)
                        self.plugins.append(plugin)
                        if hasattr(plugin, 'on_load'):
                            plugin.on_load()
                    else:
                        logging.warning(f"Plugin {plugin_name} does not have a 'Plugin' class.")
                except Exception as e:
                    logging.error(f"Error loading plugin {filename}: {e}")

    def on_start(self):
        home_dir = os.path.expanduser('~')
        self.main_interface.show_file_manager(home_dir)

        for plugin in self.plugins:
            if hasattr(plugin, 'on_start'):
                plugin.on_start()

    def on_stop(self):
        for plugin in self.plugins:
            if hasattr(plugin, 'on_stop'):
                plugin.on_stop()

if __name__ == '__main__':
    FileBrowserApp().run()
