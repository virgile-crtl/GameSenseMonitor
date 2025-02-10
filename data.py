# class Data:
#     data = {}
#     cpu = "cpu"
#     gpu = "gpu"
#     ram = "ram"
#     i = 0
#     j = 0
#     k = 0

#     def __init__(self):
#         self.get_cpu_temp()
#         self.get_gpu_temp()
#         self.get_ram_usage()
#         self.data = {"frame":{"custom-text": self.cpu+self.gpu+self.ram}}

#     def get_cpu_temp(self):
#         self.i += 1
#         self.cpu = "c" + str(self.i)
#         return self.cpu

#     def get_gpu_temp(self):
#         self.j += 1
#         self.gpu = "g" + str(self.j)
#         return self.gpu

#     def get_ram_usage(self):
#         self.k += 1
#         self.ram = "r" + str(self.k)
#         return self.ram

#     def get_data(self):
#         self.get_cpu_temp()
#         self.get_gpu_temp()
#         self.get_ram_usage()
#         self.data = {
#             "value": self.i,
#             "frame": {
#                 "custom-text": self.cpu+self.gpu+self.ram
#             }
#         }
#         return self.data
import psutil
import wmi
import time
from pynvml import (
    nvmlInit,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetTemperature,
    nvmlShutdown,
    NVML_TEMPERATURE_GPU
)

class Data:
    def __init__(self):
        self.data = {}
        self.cpu = "CPU Temp: N/A"
        self.gpu = "GPU Temp: N/A"
        self.ram = "RAM Usage: N/A"

        # Initialisation des outils WMI et NVIDIA
        self.wmi = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        self.init_gpu_monitor()
        print(self.wmi)

    def init_gpu_monitor(self):
        """Initialisation du monitoring NVIDIA GPU si disponible."""
        try:
            nvmlInit()
        except Exception:
            print("NVIDIA monitoring non disponible.")

    def get_cpu_temp(self):
        """Lecture de la température CPU via OpenHardwareMonitor.""" 
        try:
            for sensor in self.wmi.Sensor():
                if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                    self.cpu = f"CPU Temp: {sensor.Value}°C"
                    return self.cpu
        except Exception:
            self.cpu = "CPU Temp: N/A"
        return self.cpu

    def get_gpu_temp(self):
        """Récupère la température GPU pour NVIDIA et fallback pour AMD."""
        try:
            # NVIDIA GPU
            handle = nvmlDeviceGetHandleByIndex(0)
            temp = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
            self.gpu = f"NVIDIA GPU Temp: {temp}°C"
            nvmlShutdown()
        except Exception:
            # AMD Fallback ou aucun capteur NVIDIA
            try:
                for sensor in self.wmi.Sensor():
                    if sensor.SensorType == "Temperature" and "GPU" in sensor.Name:
                        self.gpu = f"AMD GPU Temp: {sensor.Value}°C"
                        return self.gpu
            except Exception:
                self.gpu = "GPU Temp: N/A"
        return self.gpu

    def get_ram_usage(self):
        """Récupère l'utilisation de la RAM."""
        ram = psutil.virtual_memory()
        self.ram = f"RAM Usage: {ram.used / (1024 ** 3):.2f} GB / {ram.total / (1024 ** 3):.2f} GB"
        return self.ram

    def update_data(self):
        """Met à jour les données CPU, GPU et RAM."""
        self.get_cpu_temp()
        self.get_gpu_temp()
        self.get_ram_usage()
        self.data = {
            "frame": {
                "custom-text": f"{self.cpu}, {self.gpu}, {self.ram}"
            }
        }

    def get_data(self):
        """Récupère les données mises à jour."""
        self.update_data()
        return self.data
