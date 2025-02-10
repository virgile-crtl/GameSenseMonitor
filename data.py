class Data:
    data = {}
    cpu = "cpu"
    gpu = "gpu"
    ram = "ram"
    i = 0
    j = 0
    k = 0

    def __init__(self):
        self.get_cpu_temp()
        self.get_gpu_temp()
        self.get_ram_usage()
        self.data = {"frame":{"custom-text": self.cpu+self.gpu+self.ram}}

    def get_cpu_temp(self):
        self.i += 1
        self.cpu = "c" + str(self.i)
        return self.cpu

    def get_gpu_temp(self):
        self.j += 1
        self.gpu = "g" + str(self.j)
        return self.gpu

    def get_ram_usage(self):
        self.k += 1
        self.ram = "r" + str(self.k)
        return self.ram

    def get_data(self):
        self.get_cpu_temp()
        self.get_gpu_temp()
        self.get_ram_usage()
        self.data = {
            "value": self.i,
            "frame": {
                "custom-text": self.cpu+self.gpu+self.ram
            }
        }
        return self.data

