import os
from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp

class FileBrowser(GridLayout):
    def __init__(self, **kwargs):
        super(FileBrowser, self).__init__(**kwargs)
        self.item_width = 100
        self.cols = 1
        self.history = []
        self.current_path = os.path.expanduser("~")
        self.calculate_columns()  # Initial column calculation
        self.size_hint_y = None  # Allow vertical resizing for scrolling
        self.bind(minimum_height=self.setter('height'))  # Adjust height based on content
        self.spacing = dp(10)
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
        
        # Bind window resize event
        Window.bind(on_resize=self.on_window_resize)
        
        self.load_directory(self.current_path)

    def load_directory(self, path=None):
        if path:
            self.history.append(self.current_path)
            if path in self.history:
                self.history.remove(path)
            self.current_path = path

        self.clear_widgets()

        # Add ".." button for back navigation
        self.add_back_button()

        # Load files and directories
        for file_path in self.list_files_and_dirs(self.current_path):
            self.add_file_or_directory(file_path)

    def add_back_button(self):
        layout = BoxLayout(orientation="vertical", size_hint=(None, None), width=self.item_width)
        img = Button(
            background_normal='img/folder.png',
            background_down='img/folder.png',
            size_hint=(None, None),
            size=(75, 80)
        )
        img.bind(on_press=self.back)
        label = Label(
            text="..",
            size_hint=(None, None),
            height=20,
            width=self.item_width,
            valign='middle',
            halign='left',
            text_size=(self.item_width, None)
        )
        label.bind(size=label.setter('text_size'))
        layout.add_widget(img)
        layout.add_widget(label)
        self.add_widget(layout)

    def add_file_or_directory(self, file_path):
        filename = os.path.basename(file_path)
        layout = BoxLayout(orientation="vertical", size_hint=(None, None), width=self.item_width)
        img_source = 'img/icons8-folder-100.png' if os.path.isdir(file_path) else self.get_file_icon(file_path)
        img = Button(
            text=file_path,
            text_size=(-1, 0),
            background_normal=img_source,
            background_down=img_source,
            halign='center',
            size_hint=(None, None),
            size=(80, 80)
        )
        img.bind(on_press=self.on_button_press)
        label = Label(
            text=filename if len(filename) < 20 else filename[:13] + "...",
            size_hint=(None, None),
            height=20,
            width=self.item_width,
            valign='middle',
            halign='center',
            text_size=(self.item_width, None)
        )
        label.bind(size=label.setter('text_size'))
        layout.add_widget(img)
        layout.add_widget(label)
        self.add_widget(layout)

    def get_file_icon(self, path):
        filename = os.path.basename(path)
        endswith = filename.lower().split('.')[-1]
        if endswith == 'txt':
            return 'img/icons8-txt-100.png'
        elif endswith in ['py', 'js', 'html', 'css', 'c', 'cpp', 'java', 'php', 'sql', 'xml', 'json']:
            return 'img/icons8-code-file-100.png'
        elif endswith in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'ico']:
            return path
        elif endswith in ['mp3', 'wav', 'ogg', 'aac', 'wma', 'flac']:
            return 'img/icons8-audio-file-100.png'
        elif endswith in ['mp4', 'avi', 'mkv', 'mov']:
            return 'img/icons8-video-100.png'
        elif endswith == 'pdf':
            return 'img/icons8-pdf-100.png'
        elif endswith in ['doc', 'docx']:
            return 'img/icons8-doc-100.png'
        elif endswith in ['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz']:
            return 'img/icons8-archive-100.png'
        else:
            return 'img/icons8-edit-file-100.png'

    def back(self, instance):
        if self.history:
            previous_path = self.history.pop()
            self.load_directory(previous_path)

    def on_button_press(self, instance):
        clicked_path = instance.text
        if os.path.isdir(clicked_path):
            self.load_directory(clicked_path)

    def calculate_columns(self):
        window_width = Window.width
        self.cols = max(3, window_width // self.item_width) - 2

    def on_window_resize(self, instance, width, height):
        self.calculate_columns()
        self.load_directory(self.current_path)  # Reload directory to update the layout

    @staticmethod
    def list_files_and_dirs(path, show_hidden=False):
        try:
            with os.scandir(path) as entries:
                if show_hidden:
                    l =  [entry.path for entry in entries]
                l = [entry.path for entry in entries if not entry.name.startswith('.')]
            # coustom sort the list so the dir are at first
            n = [x for x in l if os.path.isdir(x)]
            m = {x: os.path.basename(x).split('.')[-1] for x in l if os.path.isfile(x)}
            #sort a dict by its key
            m = dict(sorted(m.items(), key=lambda item: item[1]))
            l = n + list(m.keys())
            return l
        except Exception as e:
            print(f"Error reading directory: {e}")
            return []

class FileBrowserApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"

        # Wrap FileBrowser in ScrollView for scrolling
        root_layout = BoxLayout(orientation="vertical")
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        # Add FileBrowser inside ScrollView
        file_browser = FileBrowser()
        scroll_view.add_widget(file_browser)

        root_layout.add_widget(scroll_view)
        return root_layout

if __name__ == "__main__":
    FileBrowserApp().run()
