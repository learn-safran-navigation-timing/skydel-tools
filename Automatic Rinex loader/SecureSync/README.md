# Rinex file download tool for Skydel
This Python script allows you to download RINEX files via SecureSync and import them into Skydel. 
The tool is designed to work with a Skydel scenario that has already been built but not yet run.

## Getting Started
To get started, you will need to connect to the SecureSync server by providing the appropriate IP address, username, and password. 
Once connected, you will need to enter the date and constellations used in your Skydel scenario. 
The script will then download the corresponding RINEX file, if it exists.

## Prerequisites

To use this tool, you will need to have the following installed:

- Python 3.8 : To run this script, you need to have Python 3.8 or the later version installed on your machine. 
  If you don't have Python 3.8 installed on your machine, you can download and install it from the official website: https://www.python.org/downloads/.
  To check if python is installed, type in your command prompt : python --version.
  
  ![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/0cbede78-fdfe-419d-b430-734926a9ce9e)
  
  here, we have python version 3.10.4 installed. 

- Paramiko: This script uses Paramiko library to create SSH connections. You can install Paramiko using pip with the following command:
  pip install paramiko
  
  ![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/fa96414d-38c8-4c6b-8ccb-c0053945bdda)


- If you want to run the script on a GSG-8 unit, use the following command to update your Python version to 3.8:
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt-get install python3.8
  
- Then, you'll be able to run the script using :
  python3.8 your_script_in_python_3.8.py



## Usage

To use this tool, follow these steps:

- The script must be save in the same folder as skydeldx.
- Open Skydel and build a scenario without running the simulation.
- Run the Python script and connect to the SecureSync server by entering the appropriate IP address, username, and password.
- choose whether to download a Rinex file daily or hourly.
- The script will download the corresponding RINEX file, if it exists.
- we can find the RINEX files in the same folder as the saved script python file.

## Run the Script 
1. Next, download the script and save it to a directory on your computer. In the terminal window, navigate to the directory where the script is located. To do this, use the cd command followed by the path to the directory. For example:
cd “path of script”

![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/d86c0a0e-5276-480e-a2ee-b1973c8a5718)

N.B: The directory should be the folder location of all python script examples provided by Skydel, as well as any python scripts that were created to automate testing.
Note: If new folders are made for the python script, then the imports in the python script may need to be updated. 
2. Run the script :
Type “python [script name]” and press Enter to execute the python script.

![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/c928305f-8523-499e-b53b-df0e95ab7899)

When you run the script, it will prompt you to enter the hostname, username, and password for the SecureSync that you want to connect to. Enter this information and press Enter.
The script will then connect to the SecureSync and show you the date and constellations that were used in the scenario that you created in Skydel. It will prompt you to enter the file type (daily or hourly) that you want to download. Enter 'daily' or 'hourly' depending on the type of file you want to download.

![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/d5776129-114f-4b6d-b1da-79816442614d)

The script will then download the appropriate RINEX file based on the information entered in the Skydel scenario. The file will be saved to the same directory as the script.

Finally, the script will import the downloaded RINEX file into Skydel for use in simulations.

![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/3c18cc06-b2de-41bf-9963-7273005be8e8)

3. check on Skydel
Now, on Skydel, we can see that the RINEX files are well downloaded and imported in Skydel.
Note: if we want to find the RINEX files, we find them in the same folder as the saved script python file. for example, in my case, the files are saved here:

![image](https://github.com/learn-safran-navigation-timing/skydel-tools/assets/77835495/b2eac8d1-1e19-49f4-8ac3-9bac2c0cd3e9)








