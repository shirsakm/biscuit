import subprocess, os, sys
import tkinter as tk
import tkinter.filedialog as filedialog

from datetime import datetime

from lib.settings import Settings
from lib.utils.binder import Binder

class Base:
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.settings = Settings()
        self.bindings = self.settings.bindings

        self.active_dir = None
        self.active_file = None

        self.opened_files = []

        self.binder = Binder(base=self)

    def trace(self, e):
        time = datetime.now().strftime('• %H:%M:%S •')
        print(f'TRACE: {time} {e}')

    def refresh_dir(self):
        self.root.basepane.top.left.dirtree.create_root(self.active_dir)

    def set_active_file(self, file, exists=True):
        self.active_file = file
        self.trace(f"Active file<{self.active_file}>")

        if not exists or file not in [f[0] for f in self.opened_files]:
            print("♥♥ ", self.opened_files)
            self.add_to_open_files(file, exists)
            self.trace(f"File<{self.active_file}> was added.")
        else:
            self.root.basepane.top.right.editortabs.set_active_tab(file)

    def set_active_dir(self, dir):
        if not os.path.isdir(dir):
            return

        self.active_dir = dir
        self.refresh_dir()
        self.clean_open_files()
        self.trace(self.active_dir)

    def add_to_open_files(self, file, exists):
        self.opened_files.append([file, exists])
        self.trace(f"Opened Files {self.opened_files}")

        self.root.basepane.top.right.editortabs.update_tabs()
    
    def remove_from_open_files(self, file):
        self.opened_files.remove(file)
        self.trace(self.opened_files)
    
    def get_opened_files(self):
        return self.opened_files
    
    def clean_opened_files(self):
        self.opened_files = []
        self.trace(self.opened_files)
    
    def open_in_new_window(self, dir):
        subprocess.Popen(["python", sys.argv[0], dir])

        self.trace(f'Open in new window: {dir}')
    
    def open_new_window(self):
        subprocess.Popen(["python", sys.argv[0]])

        self.trace(f'Open new window')

    # ----- interface -----

    def newfile(self, event):
        self.set_active_file(file="Untitled", exists=False)
        self.trace('newfile event')
        pass

    def newwindow(self, event):
        self.open_new_window()
        self.trace(f"<NewWindowEvent>(.)")

    def openfile(self, event):
        self.set_active_file(filedialog.askopenfilename())
        self.trace(f"<FileOpenEvent>({self.active_file})")

    def opendir(self, event):
        self.set_active_dir(filedialog.askdirectory())
        self.trace(f"<DirOpenEvent>({self.active_dir})")
        
    def save(self, event):
        self.trace('save event')
        pass

    def saveas(self, event):
        self.trace('saveas event')
        pass

    def closefile(self, event):
        self.trace('closefile event')
        pass

    def exit(self, event):
        self.trace('exit event')
        # self.root.destroy()
        pass
    
    def undo(self, event):
        self.trace('undo event')
        pass
    
    def redo(self, event):
        self.trace('redo event')
        pass
