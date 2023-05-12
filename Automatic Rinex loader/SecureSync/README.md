# Rinex file download tool for Skydel
This Python script allows you to download RINEX files via SecureSync and import them into Skydel. 
The tool is designed to work with a Skydel scenario that has already been built but not yet run.

# Getting Started
To get started, you will need to connect to the SecureSync server by providing the appropriate IP address, username, and password. 
Once connected, you will need to enter the date and constellations used in your Skydel scenario. 
The script will then download the corresponding RINEX file, if it exists.

# Prerequisites

To use this tool, you will need to have the following installed:

- Python 3.8 : To run this script, you need to have Python 3.8 or the later version installed on your machine. 
  If you don't have Python 3.8 installed on your machine, you can download and install it from the official website: https://www.python.org/downloads/.
  To check if python is installed, type in your command prompt : python --version.
- Paramiko: This script uses Paramiko library to create SSH connections. You can install Paramiko using pip with the following command:
  pip install paramiko


# Usage

To use this tool, follow these steps:

- The script must be save in the same folder as skydeldx.
- Open Skydel and build a scenario without running the simulation.
- Run the Python script and connect to the SecureSync server by entering the appropriate IP address, username, and password.
- choose whether to download a Rinex file daily or hourly.
- The script will download the corresponding RINEX file, if it exists.
- we can find the RINEX files in the same folder as the saved script python file.





