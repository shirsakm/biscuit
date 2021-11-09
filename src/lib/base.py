import subprocess, os, sys
import tkinter as tk
import tkinter.filedialog as filedialog

from datetime import datetime

from .settings import Settings
from .utils.binder import Binder
from .utils.events import Events

from .components.git import GitCore


class Base:
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.appdir = root.appdir
        self.settings = Settings(self)
        self.bindings = self.settings.bindings

        self.git_found = False
        self.git = GitCore(self)
        print(self.git.get_version())

        self.active_dir = None
        self.active_dir_name = None
        self.active_file = None

        # Opened files
        # [file, exists]
        self.opened_files = []

        self.events = Events(self)
        self.binder = Binder(base=self)

        self.binder.bind('<Control-`>', self.toggle_terminal)
        self.binder.bind('<Control-b>', self.toggle_active_side_pane)

    def after_initialization(self):
        self.refresh()
    
    def refresh(self):
        self.update_statusbar_ln_col_info()
        self.update_editor_tabs_pane()
    
    def get_app_dir(self):
        return self.appdir
    
    def get_config_path(self, config_file):
        return os.path.join(self.appdir, 'config', config_file)
    
    def get_themes_path(self, theme_name):
        return os.path.join(self.appdir, 'config/themes', theme_name)
    
    def get_bindings_path(self, bindings_file):
        return os.path.join(self.appdir, 'config/bindings', bindings_file)

    def get_res_path(self, res_file):
        return os.path.join(self.appdir, 'res', res_file)

    def trace(self, e):
        time = datetime.now().strftime('• %H:%M:%S •')
        print(f'TRACE {time} {e}')
    
    def set_git_found(self, found):
        self.git_found = found

    def refresh_dir(self):
        self.root.primarypane.basepane.dirtree.create_root(self.active_dir)

    def set_active_file(self, file, exists=True):
        if not file:
            return

        self.active_file = file
        self.trace(f"Active file<{self.active_file}>")

        if not exists or file not in [f[0] for f in self.opened_files]:
            self.add_to_open_files(file, exists)
            self.trace(f"File<{self.active_file}> was added.")
        else:
            self.root.primarypane.basepane.right.top.editortabs.tabs.set_active_tab(file)
        self.refresh()
        

    def set_active_dir(self, dir):
        if not os.path.isdir(dir):
            return

        self.active_dir = dir
        self.active_dir_name = os.path.basename(dir)

        self.check_git()
        self.update_git()
        
        self.refresh_dir()
        self.clean_opened_files()
        self.refresh()
        
        self.trace(self.active_dir)

    def add_to_open_files(self, file, exists):
        self.opened_files.append([file, exists])
        self.trace(f"Opened Files {self.opened_files}")

        self.root.primarypane.basepane.right.top.editortabs.tabs.update_tabs()
    
    def close_active_file(self):
        if self.active_file:
            self.remove_from_open_files(self.active_file)
            self.root.primarypane.basepane.right.top.editortabs.tabs.remove_tab(self.active_file)

            self.refresh()
            self.trace(f"<CloseActiveFileEvent>({self.active_file})")
    
    def remove_from_open_files(self, file):
        self.opened_files = [f for f in self.opened_files if f[0] != file]
        self.trace(f"Removed from open files: {file}")
        self.root.primarypane.basepane.right.top.editortabs.tabs.update_tabs()
        
        self.refresh()
        self.trace(self.opened_files)
    
    def get_opened_files(self):
        return self.opened_files
    
    def clean_opened_files(self):
        self.opened_files = []
        self.active_file = None
        self.trace(f"<ClearOpenFilesEvent>({self.opened_files})")
    
    def open_in_new_window(self, dir):
        subprocess.Popen(["python", sys.argv[0], dir])

        self.trace(f'Opened in new window: {dir}')
    
    def open_new_window(self):
        subprocess.Popen(["python", sys.argv[0]])

        self.trace(f'Opened new window')
    
    def toggle_terminal(self, *args):
        self.root.primarypane.basepane.right.terminal.toggle()
    
    def toggle_active_side_pane(self, *args):
        self.root.primarypane.sidebar.toggle_active_pane()
    
    def update_editor_tabs_pane(self):
        self.root.primarypane.basepane.right.top.editortabs.update_panes()
    
    def check_git(self):
        self.git.open_repo()

    def update_git(self):
        if self.git_found:
            self.root.statusbar.configure_git_info(True)
            self.update_statusbar_git_info()

            self.root.primarypane.basepane.git.enable()
        else:
            self.root.statusbar.configure_git_info(False)
            self.root.primarypane.basepane.git.disable()

    def update_statusbar_git_info(self):
        self.root.statusbar.configure_git_info(True)
        self.root.statusbar.set_git_info(self.git.get_active_branch())

    def update_statusbar_ln_col_info(self):
        if self.active_file:
            self.root.statusbar.configure_editmode(True)
            active_text = self.root.primarypane.basepane.right.top.editortabs.tabs.get_active_tab().content.text
            self.root.statusbar.set_line_col_info(active_text.line, active_text.column, active_text.get_selected_count())
        else:
            self.root.statusbar.configure_editmode(False)