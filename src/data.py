import psutil, clr
from datetime import datetime
from utils import get_resource_path

try:
    clr.AddReference(get_resource_path("assets\\lib\\LibreHardwareMonitorLib.dll"))
except Exception as e:
    my_e = type(e)(f"Error while loading the dll.\n{e}")
    raise my_e from e

from LibreHardwareMonitor.Hardware import Computer # type: ignore

class Data:

    def __init__(self):
        try:
            self.computer = Computer()
            self.computer.IsGpuEnabled = True
            self.computer.IsCpuEnabled = True
            self.computer.Open()
            for hardware in self.computer.Hardware:
                if hardware.HardwareType.ToString().find("Cpu") != -1:
                    self.cpu = hardware
                if hardware.HardwareType.ToString().find("GpuNvidia") != -1:
                    self.gpu = hardware
        except Exception as e:
            my_e = type(e)(f"Error accessing monitoring data.\n{e}")
            raise my_e from e

    def get_hour(self):
        try:
            return datetime.now().strftime("%H:%M %d/%m")
        except Exception as e:
            return "N/A"

    def get_cpu_temp(self):
        try:
            self.cpu.Update()
            for sensor in self.cpu.Sensors:
                if sensor.Name.find("Package") != -1 and sensor.SensorType.ToString().find("Temperature") != -1:
                    return str(int(sensor.Value)) + "°C"
        except Exception as e:
            return "N/A"

    def get_gpu_temp(self):
        try:
            self.gpu.Update()
            for sensor in self.gpu.Sensors:
                if sensor.Name.find("Hot Spot") != -1:
                    return str(int(sensor.Value)) + "°C"
        except Exception as e:
            return "N/A"

    def get_ram_usage(self):
        try:
            return str(psutil.virtual_memory().percent) + "%"
        except Exception as e:
            return "N/A"

    def get_all_info(self):
        return {
            "cpu_temp": self.get_cpu_temp(),
            "gpu_temp": self.get_gpu_temp(),
            "ram_usage": self.get_ram_usage(),
            "hour": self.get_hour()
        }

