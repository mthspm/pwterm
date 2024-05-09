import psutil
import GPUtil
import netifaces as ni
import wmi
from alive_progress import alive_bar

class Analyser(object):
    def __init__(self):
        pass

    @staticmethod
    def get_disk_info(path:str='/'):
        """Get disk information | to search others drivers, try D:, E:, F:, etc."""
        disk = psutil.disk_usage(path)
        gb_format = lambda x: "{}{}".format(round(x / (1024 * 1024 * 1024)), "GB")
        total = gb_format(disk.total)
        used = gb_format(disk.used)
        free = gb_format(disk.free)
        percent = "{}{}".format(round(disk.percent), "%")
        print(f"Total: {total}\nUsed: {used}\nFree: {free}\nPercent: {percent}")

    @staticmethod
    def get_cpu_info():
        """Get CPU information."""
        cpu = psutil.cpu_freq()
        gb_format = lambda x: "{}{}".format(x / 1000, "GHz")
        current = gb_format(cpu.current)
        min = gb_format(cpu.min)
        max = gb_format(cpu.max)
        percent = "{}{}".format(psutil.cpu_percent(), "%")
        print(f"Current: {current}\nMin: {min}\nMax: {max}\nPercent: {percent}")

    @staticmethod
    def get_memory_info():
        """Get memory information."""
        memory = psutil.virtual_memory()
        gb_format = lambda x: "{}{}".format(round(x / (1024 * 1024 * 1024)), "GB")
        total = gb_format(memory.total)
        available = gb_format(memory.available)
        percent = "{}{}".format(round(memory.percent), "%")
        used = gb_format(memory.used)
        free = gb_format(memory.free)
        print(f"Total: {total}\nAvailable: {available}\nPercent: {percent}\nUsed: {used}\nFree: {free}")

    @staticmethod
    def get_gpu_info():
        """Get GPU information."""
        gpu = GPUtil.getGPUs()
        name = gpu[0].name
        memory = "{}{}".format(gpu[0].memoryTotal, "MB")
        used = "{}{}".format(gpu[0].memoryUsed, "MB")
        temperature = "{}{}".format(gpu[0].temperature, "°C")
        print(f"Name: {name}\nMemory: {memory}\nUsed: {used}\nTemperature: {temperature}")

    @staticmethod
    def get_default_gateway():
        default_gateway = None
        gws = ni.gateways()

        if 'default' in gws and ni.AF_INET in gws['default']:
            default_gateway = gws['default'][ni.AF_INET][0]

        return default_gateway

    @staticmethod
    def get_motherboard_info():
        """Get motherboard information."""
        motherboard = wmi.WMI().Win32_BaseBoard()[0]
        manufacturer = motherboard.Manufacturer
        product = motherboard.Product
        serial = motherboard.SerialNumber
        version = motherboard.Version
        qualifiers = motherboard.qualifiers
        print(f"Manufacturer: {manufacturer}\nProduct: {product}\nSerial: {serial}\nVersion: {version}\nQualifiers: {qualifiers}")


    def get_network_info(self):
        """Get network information."""
        network = psutil.net_if_addrs()
        ip_machine = network['Ethernet'][0].address
        ipv4 = network['Ethernet'][1].address
        ip_mask = network['Ethernet'][1].netmask
        ipv6 = network['Ethernet'][2].address
        temp_ipv6 = network['Ethernet'][3].address
        localing_ipv6 = network['Ethernet'][4].address
        gateway = self.get_default_gateway()
        print(f"IP Machine: {ip_machine}\nIPv4: {ipv4}\nIP Mask: {ip_mask}\nIPv6: {ipv6}\nTemp IPv6: {temp_ipv6}\nLocallink IPv6: {localing_ipv6}\nGateway: {gateway}")

    @staticmethod
    def get_drivers_info():
        """Get drivers information."""
        drivers = wmi.WMI().Win32_PnPSignedDriver()
        drivers_data = [["Device", "Manufacturer", "DriverVersion", "DriverDate"]]
        filled = []
        with alive_bar(len(drivers)) as bar:
            for driver in drivers:
                bar()
                date = driver.DriverDate
                if driver.DeviceName is not None and date is not None and driver.DeviceName not in filled:
                    date = f"{date[0:4]}-{date[4:6]}-{date[6:8]} {date[8:10]}:{date[10:12]}:{date[12:14]}"
                    drivers_data.append([driver.DeviceName, driver.Manufacturer, driver.DriverVersion, date])
                    filled.append(driver.DeviceName)

        max_length = max([len(str(i)) for sublist in drivers_data for i in sublist])
        for driver in drivers_data:
            print(" ".join([i.ljust(max_length) for i in driver]))
