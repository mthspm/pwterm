import json
import os
from pathlib import Path
from alive_progress import alive_bar
from .analyser import Analyser

class Cleaner(object):
    def __init__(self):
        self.paths = None
        self.analyser = Analyser()
        self.load_paths()

    def load_paths(self):
        path = Path(__file__).parent / 'caches_files.json'
        with open(path, 'r') as file:
            self.paths = json.load(file)

    @staticmethod
    def clear_folder(path, user_profile=False, system_drive=False):
        if user_profile:
            temp_path = os.path.join(os.environ['USERPROFILE'], path)
        elif system_drive:
            temp_path = os.path.join((os.environ['SystemDrive'] + '\\'), path)
        else:
            temp_path = path

        if os.path.exists(temp_path):
            for root, dirs, files in os.walk(temp_path, topdown=False):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        print(e)
                for dir in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir))
                    except Exception as e:
                        print(e)
        else:
            print(f"Path {temp_path} not found.")

    def clear(self):
        """Clear cache files."""
        with alive_bar(len(self.paths)) as bar:
            for app in self.paths.values():
                for path in app['paths'].values():
                    self.clear_folder(path, app['user_profile'], app['system_drive'])
                bar()