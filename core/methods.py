from .cleaner import Cleaner, Analyser
from .iptracker import Tracker
import inspect
import sys
import os

class Methods(object):
    def __init__(self):
        self.cleaner: Cleaner = Cleaner()
        self.analyser: Analyser = Analyser()
        self.tracker: Tracker = Tracker()
        self.methods: dict[str, callable] = {}
        self.setup()
        self.docs: dict[str, str] = {name: method.__doc__ for name, method in self.methods.items()}

    def add_method(self, name, method):
        self.methods[name] = method

    def get_method(self, name):
        method = self.methods.get(name)
        if not method:
            return None
        return method

    def run_method(self, *args):
        method = self.get_method(args[0][0])
        try:
            if method:
                result = method(*args[0][1:])
                if result:
                    print(result)
                return True
        except Exception as e:
            raise e
        return False

    def setup(self):
        self.add_method('help', self.help)
        self.add_method('cls', self.cls)
        self.add_method('exit', self.exit)
        self.add_method('quit', self.exit)
        self.add_method('clear', self.cleaner.clear)
        self.add_method('disk', self.analyser.get_disk_info)
        self.add_method('cpu', self.analyser.get_cpu_info)
        self.add_method('memory', self.analyser.get_memory_info)
        self.add_method('network', self.analyser.get_network_info)
        self.add_method('gpu', self.analyser.get_gpu_info)
        self.add_method('drivers', self.analyser.get_drivers_info)
        self.add_method('motherboard', self.analyser.get_motherboard_info)
        self.add_method('ip', self.tracker.get_ip_info)
        self.add_method('ping', self.tracker.ping)

    def help(self, func:callable=None):
        """Show available commands or help for a specific command."""
        if not func:
            print("Available commands:")
            for key, value in self.docs.items():
                key_length = len(key)
                print(f"{key}{' ' * (20 - key_length)}{value}")
        else:
            try:
                method = self.get_method(func)
                params = inspect.signature(method).parameters
                print(f"{func}: {self.docs[func]}")
                for name, param in params.items():
                    df = param.default if param.default is not inspect.Parameter.empty else 'No default'
                    print(f"arg: {name}, type: {param.annotation}, default: {df}")
            except TypeError:
                print(f"Error: built-in function '{func}' not found.")
    @staticmethod
    def exit():
        """Exit the terminal."""
        input("Exiting the terminal. Press any key to continue...\n")
        sys.exit()

    @staticmethod
    def cls():
        """Clear the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')