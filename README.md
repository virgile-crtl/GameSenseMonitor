# GameSenseMonitor

A Python application that displays monitoring information on the **SteelSeries Arctis Nova Pro** headset screen using the Gamesense SDK.

## Features

- Displays temperature data for **CPU**, **GPU**, **RAM** and more.
- Customizable display on the headset screen via the Gamesense SDK.

## Prerequisites

- **Python 3.x**
- [SteelSeries Engine](https://steelseries.com/engine)

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:virgile-crtl/GameSenseMonitor.git
   ```

2. **Run the installer**:

   Run the GameSenseMonitor_installer.exe to install the application on your system.

## Compilation

1. Navigate to the project directory:

   ```bash
   cd GameSenseMonitor
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Compile the application** using Nuitka:

   Before using the installer, compile the Python application into a standalone executable with the following command:

   ```bash
   py -m nuitka --onefile --standalone --windows-console-mode=disable --include-data-files=assets/lib/LibreHardwareMonitorLib.dll=lib/ --include-data-files=assets/icons/appIcon.ico=icons/ --include-data-files=assets/config/appConfig.json=config/ --follow-imports --windows-icon-from-ico=assets/icons/appIcon.ico --windows-uac-admin --output-filename=GameSenseMonitor.exe src/main.py
   ```

## Avoiding Detection by Microsoft Defender

Microsoft Defender may detect the application as a potential threat, especially when using custom executables. To prevent the application from being deleted or flagged, users can add an exclusion for the installation folder.

Run the following PowerShell command in Admin:

```bash
Add-MpPreference -ExclusionPath "C:\Program Files\GameSenseMonitor"
```

If you changed the installation path, be sure to replace `"C:\Program Files\GameSenseMonitor"` with the actual path where the program is installed.

## Contributing

Feel free to open issues or pull requests. Please follow the project's coding conventions.
