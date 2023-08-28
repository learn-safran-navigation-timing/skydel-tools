# Rinex File Download Tool

This script allows you to download RINEX files from websites and import them into Skydel automatically.

## Introduction
The Rinex File Download Tool is a Python script that connects to Skydel, retrieves simulation data (date and constellations), and downloads the corresponding RINEX files from specific websites. It then decompresses the files and imports them into Skydel for further use.

## Prerequisites
- Python 3.8 or above
- Skydel
- Required Python packages (listed in `requirements.txt`)

## Usage
1. First, make sure to build a scenario on Skydel without running the simulation.
2. Run the script.
3. The script will Connect to Skydel.
4. The script will retrieve the date and constellations played on Skydel.
5. Based on the simulation information, the script will download the corresponding RINEX file if it exists.
6. After downloading, the script will decompress the files and import them into Skydel.

## Setup
1. Clone this repository:
git clone <repository_url>

2. Install the required Python packages:
pip install -r requirements.txt

3. Packages installation: unlzw3
unlz3 is a library to decompress data that has been compressed using the LZ3 compression algorithm. LZ3 is a lossless data compression algorithm that is known for its fast decompression speed and low memory requirements.

You can download the unlz3 library from the official website at: [unlzw3·PyPI](https://pypi.org/project/unlzw3/)
Once you've downloaded the unlz3 library, extract the files from the downloaded.tar.gz file. You can use a tool like 7-Zip or WinRAR to extract the files. Extract the files to a directory of your choice.

## Configuration
Before running the script, make sure to configure the following settings:

- Skydel settings: Ensure that SKYDEL settings are properly configured before running the script ( date and signals).

## Running the Script
1. Open a command prompt window, navigate your python script by typing “cd [.py folder location]”, and press Enter.
![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/0c847f68-392f-48fa-b71f-dd2619af68e0)

N.B: The directory should be the folder location of all python script examples provided by Skydel, as well as any python scripts that were created to automate testing. Note: If new folders are made for the python script, then the imports in the python script may need to be updated. Type “python [script name]” and press Enter to execute the python script.

2. The script will then run and the files will be downloaded to the directory where the script is saved.
![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/a398117b-c26b-4e9f-940e-ac4764cafd3a)


3. On Skydel, we find that the files are successfully imported

![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/ff0d2eab-9919-4030-968f-8321736ef234)




