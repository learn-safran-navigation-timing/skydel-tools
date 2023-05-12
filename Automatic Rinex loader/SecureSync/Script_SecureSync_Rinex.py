# This script allows you to download RINEX files via the SecureSych and imported its in skydel.
# We must first build a scenario on skydel without running the simulation.
# After, We connect to one of the securesynch by putting the right hosname, username and password
# Now, from the informations (date and constellations) entered in the scenario, 
# The script will download the rinex file corresponding to this scenario if it exists.


# import................
from skydelsdx import *
import datetime
from datetime import date
from skydelsdx.commands import *
from ftplib import FTP_TLS
import gzip
import shutil
import urllib.request as request
from contextlib import closing
import paramiko
import socket
from skydelsdx.remotesimulator import RemoteSimulator
import os

print()
print("*** Welcome to our Rinex file download tool ***")
print()

#connection with skydel
sim = RemoteSimulator()

try:
    sim.connect()
except socket.error as err:
    if isinstance(err, ConnectionRefusedError):
        print("Please configure SKYDEL settings first, then restart the script")
        sys.exit()
    else:
        print("An unexpected socket error occurred:", err)
        sys.exit()
        
print("Please provide the following information to connect to SecureSync")
print ("")

#connection with SecureSync
while True:
    try :
        # Requesting login information
        print("Please provide the following information to connect to SecureSync")
        print ()
        hostname = str(input ("Enter the IP address : "))
        username = str(input ("enter the username : "))
        password = str(input ("enter the password : "))

        # connection with the SecureSync
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, username =username, password = password, port = 22, allow_agent=False,look_for_keys=False)

        stdin,stdout,stderror=ssh_client.exec_command('ls')
        stdout.readlines()
        print()
        print('connection established successfully')
        connected = True
        # exit the while loop if the connection is established
        break


    except paramiko.ssh_exception.AuthenticationException :
        print("Invalid username or password")

    except (socket.gaierror, TimeoutError) :
        print("Invalid IP address")

    except:
        print("Authentification failed")

    print("Connection failed. Please try again.")


# Show the data of the date we played on skydel
res = sim.call(GetGpsStartTime())
print("the date of my simulation :")
print(res.startTime())
print("the year of my simulation :")
year = res.startTime().year
print(year)
print("the month of my simulation :")
month = res.startTime().month
print(month)
print("the day of my simulation : ")
day = (res.startTime().day)

current_date = datetime.date.today()
simulation_date = res.startTime().date()
if simulation_date > current_date:
    print("Simulation date is in the future. Please choose an earlier date in sKydel.")
    exit()

#calculation of the number of days
#day:  the number of days in the month
#Day : the number of days in the year  
d1 = date(year, month, day)
d0 = date(year, 1, 1)
delta = d1-d0
Day = delta.days + 1

#conversion of days of the year to format ---> ddd 
Day = "{:03d}".format(Day)

print("le {}-{}-{} is the {}rd day of the year".format(year, month, day, Day))

#Show the different constellations we played on skydel
ouput = 0
outputIdx = 0

try :
    MyId = sim.call(GetAllModulationTargets()).ids()
    sig = sim.call(GetModulationTargetSignals(ouput,MyId[outputIdx])).signal()
    print("the constellations played during the simulation are: {}".format(sig))
except IndexError :
    print()
    print("Please choose first a radio card and the constellations you want to play")
    sig = [] # initialized as an empty list if an exception is raised and the program will not crash when checking if "L1CA" is in sig


#if the signal is a  GPS
gps_signals = ["L1CA", "L1C", "L1P", "L1ME", "L1MR", "L2C", "L2P", "L2ME", "L2MR", "L5"]

# check if the signal is a GPS
if any(signal in sig for signal in gps_signals):
    print ("======================================================================================================")
    print("the signal is a GPS")

    try:

        # Prompt the user to choose the file type to download
        while True:
            file_type = input("Enter file type (daily/hourly): ")
            if file_type.lower() in ["daily", "hourly"]:
                break  # Exit the loop if the file type is valid
        else:
            print("Invalid file type, please try again.")

        # last forler where the Rinex is located = YY+n
        new_year = ""
        for i in range(len(str(year))):
            if i != 1 and i != 2:
                new_year = new_year + str(year)[i]
        dossier = new_year + "n"

        sftp = ssh_client.open_sftp()

        # Download the appropriate file based on the user's input
        if file_type.lower() == "daily":
            file = 'spec' + str(Day) + str(0) + '.' + dossier + '.Z'
            link = '/pub/gps/data/daily/' + str(year) + '/' + str(Day) + '/' + dossier + '/' + file
        else:
            file = 'hour' + str(Day) + str(0) + '.' + dossier + '.Z'
            link = '/pub/gps/data/hourly/' + str(year) + '/' + str(Day) + '/' + dossier + '/' + file

        sftp.get(link, file)

        sftp.close()

        print(f"sftp:/{link}........Succesfully")
        print(f"The Rinex file name : {file}")
        print("{} successfully downloaded".format(file))

        # Unzip the rinex file
        file_unzip = file.replace(".Z", "")

        with gzip.open(file, 'rb') as f_in:
            with open(file_unzip, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("{} Successfully decompressed".format(file))



        # Import the Rinex file in Skydel
        try:
            # Get the current working directory
            current_dir = os.getcwd()

            # Look for the Rinex file in a subdirectory of the current working directory
            rinex_dir = os.path.join(current_dir, "")
            path = os.path.join(rinex_dir, file_unzip)

            rinex = sim.call(ImportConstellationParameters("GPS", path, 0, "Default"))
        except UnicodeDecodeError:
            pass
        print("{} Successfully imported in Skydel".format(file))

    except FileNotFoundError:
        print(f"sftp:/{link}........Failed")
        print("This rinex file doesn't exist")
    
        

#if the signal is a Glonass     
if "G1" in sig:
    print ("======================================================================================================")
    print("the signal is a GLONASS")
    
    try:
        # Prompt the user to choose the file type to download
        while True:
            file_type = input("Enter file type (daily/hourly): ")
            if file_type.lower() in ["daily", "hourly"]:
                break  # Exit the loop if the file type is valid
            else:
                print("Invalid file type, please try again.")

        # last forler where the Rinex is located = YY+g
        new_year = ""
        for i in range(len(str(year))):
            if i != 1 and i != 2:
                new_year = new_year + str(year)[i]
        dossier = new_year + "g"

        sftp = ssh_client.open_sftp()

        # Download the appropriate file based on the user's input
        if file_type.lower() == "daily":
            file = 'spec' + str(Day) + str(0) + '.' + dossier + '.Z'
            link = '/pub/glonass/data/daily/' + str(year) + '/' + str(Day) + '/' + dossier + '/' + file
        else:
            file = 'hour' + str(Day) + str(0) + '.' + dossier + '.Z'
            link = '/pub/glonass/data/hourly/' + str(year) + '/' + str(Day) + '/' + dossier + '/' + file

        sftp.get(link, file)

        sftp.close()

        print(f"sftp:/{link}........Succesfully")
        print(f"The Rinex file name : {file}")
        print("{} successfully downloaded".format(file))

        # Unzip the rinex file
        file_unzip = file.replace(".Z", "")

        with gzip.open(file, 'rb') as f_in:
            with open(file_unzip, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("{} Successfully decompressed".format(file))

        # Import the Rinex file in Skydel
        try:
            # Get the current working directory
            current_dir = os.getcwd()

            # Look for the Rinex file in a subdirectory of the current working directory
            rinex_dir = os.path.join(current_dir, "")
            path = os.path.join(rinex_dir, file_unzip)

            rinex = sim.call(ImportConstellationParameters("GLONASS", path, 0, "Default"))
        except UnicodeDecodeError:
            pass
        print("{} Successfully imported in Skydel".format(file))

    except FileNotFoundError:
        print(f"sftp:/{link}........Failed")
        print("This rinex file doesn't exist")

    
#if the signal is a  Galileo  
if "E1" in sig:
    print ("======================================================================================================")
    print("the signal is a GALILEO")

    try:
        # Prompt the user to choose the file type to download
        while True:
            file_type = input("Enter file type (daily/hourly): ")
            if file_type.lower() in ["daily", "hourly"]:
                break  # Exit the loop if the file type is valid
            else:
                print("Invalid file type, please try again.")


        # last forler where the Rinex is located = YY+l
        new_year = ""
        for i in range(len(str(year))):
            if i != 1 and i != 2:
                new_year = new_year + str(year)[i]
        dossier = new_year + "l"

        sftp = ssh_client.open_sftp()

        # Download the appropriate file based on the user's input
        if file_type.lower() == "daily":
            file = 'spec' + str(Day) + str(0) + '.' + dossier + '.Z'
            link = '/pub/galileo/data/daily/' + str(year) + '/' + str(Day) + '/' + dossier + '/' + file
        else:
            file = 'hour' + str(Day) + str(0) + '.' + dossier + '.Z'
            link = '/pub/galileo/data/hourly/' + str(year) + '/' + str(Day) + '/' + dossier + '/' + file

        sftp.get(link, file)

        sftp.close()

        print(f"sftp:/{link}.........Succesfully")
        print(f"The Rinex file name : {file}")
        print("{} successfully downloaded".format(file))

        # Unzip the rinex file
        file_unzip = file.replace(".Z", "")

        with gzip.open(file, 'rb') as f_in:
            with open(file_unzip, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("{} Successfully decompressed".format(file))

        # Import the Rinex file in Skydel
        try:
            # Get the current working directory
            current_dir = os.getcwd()

            # Look for the Rinex file in a subdirectory of the current working directory
            rinex_dir = os.path.join(current_dir, "")
            path = os.path.join(rinex_dir, file_unzip)

            rinex = sim.call(ImportConstellationParameters("Galileo", path, 0, "Default"))
        except UnicodeDecodeError:
            pass
        print("{} Successfully imported in Skydel".format(file))

    except FileNotFoundError:
        print(f"sftp:/{link}........Failed")
        print("This rinex file doesn't exist")


#if the signal is a beidou
if "B1" in sig:
    print ("======================================================================================================")
    print("the signal is a BEIDOU")
    
    try:
        # Prompt the user to choose the file type to download
        while True:
            file_type = input("Enter file type (daily/hourly): ")
            if file_type.lower() in ["daily", "hourly"]:
                break  # Exit the loop if the file type is valid
            else:
                print("Invalid file type, please try again.")

        # last forler where the Rinex is located = YY+f
        new_year = ""
        for i in range(len(str(year))):
            if i != 1 and i != 2:
                new_year = new_year + str(year)[i]
        dossier = new_year + "f"

        sftp = ssh_client.open_sftp()

        # Download the appropriate file based on the user's input
        if file_type.lower() == "daily":
            file = 'spec' + str(Day) + str(0) + '.' + dossier + '.Z'
            link = '/pub/beidou/data/daily/' + str(year) + '/' + str(Day) + '/' + dossier + '/' + file
        else:
            file = 'hour' + str(Day) + str(0) + '.' + dossier + '.Z'
            link = '/pub/beidou/data/hourly/' + str(year) + '/' + str(Day) + '/' + dossier + '/' + file

        sftp.get(link, file)

        sftp.close()

        print(f"sftp:/{link}........Succesfully")
        print(f"The Rinex file name : {file}")
        print("{} successfully downloaded".format(file))

        # Unzip the rinex file
        file_unzip = file.replace(".Z", "")

        with gzip.open(file, 'rb') as f_in:
            with open(file_unzip, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("{} Successfully decompressed".format(file))

        # Import the Rinex file in Skydel
        try:
            # Get the current working directory
            current_dir = os.getcwd()

            # Look for the Rinex file in a subdirectory of the current working directory
            rinex_dir = os.path.join(current_dir, "")
            path = os.path.join(rinex_dir, file_unzip)

            rinex = sim.call(ImportConstellationParameters("Beidou", path, 0, "Default"))
        except UnicodeDecodeError:
            pass
        print("{} Successfully imported in Skydel".format(file))

    except FileNotFoundError:
        print(f"sftp:/{link}........Failed")
        print("This rinex file doesn't exist")

            
