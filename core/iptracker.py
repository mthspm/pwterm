from dotenv import load_dotenv
import ipdata
import os
import subprocess

class Tracker(object):
    def __init__(self):
        load_dotenv()
        self.ipdata = ipdata.IPData(os.getenv('IPDATA_KEY'))

    def get_ip(self, ip:int=None):
        if ip:
            data = self.ipdata.lookup(str(ip))
        else:
            data = self.ipdata.lookup()
        return data

    def get_ip_info(self, ip:int=None):
        """Get information about an IP address."""
        data = self.get_ip(ip)
        for key, value in data.items():
            print(f"{key}: {value}")

    @staticmethod
    def ping(ip:str, count:int):
        """Ping an IP address."""
        process = subprocess.Popen(['ping', '-n', str(count), str(ip)], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8').strip())

        process.stdout.close()
        process.wait()
