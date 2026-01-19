# 🎮 GameSenseMonitor

![GitHub release](https://img.shields.io/github/v/release/virgile-crtl/GameSenseMonitor)
![GitHub License](https://img.shields.io/github/license/virgile-crtl/GameSenseMonitor)

A Python application that displays monitoring information on the **SteelSeries Arctis Nova Pro** headset screen using the GameSense SDK.

---

## ✨ Features

- Displays temperature data for **CPU**, **GPU**, **RAM**, and more.
- Customizable display on the headset screen via the GameSense SDK.
- Lightweight and runs in the background.
- Built using [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor).

---

## 🖥️ Installation

👉 [**Download the latest release**](https://github.com/virgile-crtl/GameSenseMonitor/releases/latest)

> ⚠️ Please ensure that the **SteelSeries Engine** is installed and running.

---

## 🧰 Prerequisites for development

- **Python 3.x**
- [SteelSeries Engine](https://steelseries.com/engine)
- [Nuitka](https://nuitka.net/) (for compilation)

---

## 🛠️ Build from source

1. Clone and navigate to the project directory:

   ```bash
   git clone https://github.com/virgile-crtl/GameSenseMonitor.git
   cd GameSenseMonitor
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Compile the application** using Nuitka:

   Before using the installer, compile the Python application into a standalone folder with the following command:

   ```bash
   py -m nuitka --standalone --windows-console-mode=disable \
     --include-data-files=assets/lib/LibreHardwareMonitorLib.dll=assets/lib/ \
     --include-data-files=assets/icons/appIcon.ico=assets/icons/ \
     --include-data-files=assets/config/appConfig.json=assets/config/ \
     --follow-imports --windows-icon-from-ico=assets/icons/appIcon.ico \
     --windows-uac-admin --output-filename=GameSenseMonitor.exe src/main.py
   ```

   This produces `GameSenseMonitor.dist` containing `GameSenseMonitor.exe` and all dependencies.

## 🤝 Contributing

Contributions are welcome!
Feel free to open issues to report bugs or suggest features, or submit pull requests.
Please follow the project's coding conventions and write clear, well-documented code.
Thank you for helping improve GameSenseMonitor! 🙏
