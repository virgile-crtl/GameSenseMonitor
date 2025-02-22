import psutil
import pynvml

class Data:

    def __init__(self):
        pynvml.nvmlInit()
        self.gpu_info = pynvml.nvmlDeviceGetHandleByIndex(0)

    def get_cpu_temp(self):
        self.cpu = "N/A"
        return self.cpu

    def get_gpu_temp(self):
        self.gpu = str(pynvml.nvmlDeviceGetTemperature(self.gpu_info, pynvml.NVML_TEMPERATURE_GPU))
        return self.gpu

    def get_ram_usage(self):
        self.ram = str(psutil.virtual_memory().percent)
        return self.ram
