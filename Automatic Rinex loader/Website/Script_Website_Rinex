# This script allows you to download RINEX files via websites and imported its in skydel automatically.
# We must first build a scenario on skydel without running the simulation.
# After connecting to skydel to retrieve the date and constellations played on Skydel
# Now, from the informations (date and constellations) entered in the scenario, 
# The script will download the rinex file corresponding to this scenario if it exists.
# At the end the files will be decompressed and imported on Skydel.

#import of commandes
from skydelsdx.commands import *
import datetime
from datetime import date
from skydelsdx import *
from ftplib import FTP_TLS
import gzip
import shutil
import urllib.request as request
from contextlib import closing
import unlzw3
import os
import socket
import urllib
import ftplib

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

#Show the data of the date we played on skydel
res = sim.call(GetGpsStartTime())
print(f"the date of my simulation :")
print(res.startTime())
print("the year of my simulation :")
year = res.startTime().year
print(year)
print("the month of my simulation :")
month = res.startTime().month
print(month)
print("the day of my simulation : ")
day = (res.startTime().day)
print(day)

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
    print("The constellations played during the simulation are: {}".format(sig))
except IndexError :
    print()
    print("Please choose first a radio card and the constellations you want to play")
    sig = [] # initialized as an empty list if an exception is raised and the program will not crash when checking if "L1CA" is in sigat(sig))

#if the signal is a  GPS
if "L1CA" in sig:
    print ("======================================================================================================")
    print("The signal is a gps")
    
    
    try :

        # last forler where the Rinex is located = YY+n
        new_year = ""
        for i in range(len(str(year))):
            if i !=1 & i !=2:
                new_year = new_year  + str(year)[i] 
                folder = new_year + "n"
                
        #connection ftp
        ftp_host = 'gdc.cddis.eosdis.nasa.gov'
        ftp_path = '/pub/gps/data/daily/'+ str(year) + '/' + str(Day) + '/' + folder 
        local_path = "brdc"+ str(Day)+str(0)+"."+str(folder)

        ftp = FTP_TLS(ftp_host)
        ftp.login()
        ftp.prot_p()
        ftp.cwd(ftp_path)
        files = ftp.nlst()
        Rinex_file = "brdc"+ str(Day)+str(0)+"."+str(folder)
               
        # Download .Z file if it exists
        if Rinex_file + ".Z" in files:
            with open(Rinex_file + ".Z", 'wb') as f:
                ftp.retrbinary(f"RETR {Rinex_file}.Z", f.write)
            print("The file can be foud on the CDDIS NASA website : 'gdc.cddis.eosdis.nasa.gov' ")

            print(f"ftp://{ftp_host}{ftp_path}")
            print(f"The RINEX file name : {Rinex_file}.Z ")
            print(f"{Rinex_file}.Z successfully downloaded.")

            # Decompress the .Z file
            compressed_path = local_path + ".Z"
            decompressed_path = local_path
            with open(decompressed_path, 'wb') as f_out:
                with open(compressed_path, 'rb') as f_in:
                    decompressed_data = unlzw3.unlzw(f_in.read())
                    f_out.write(decompressed_data)
            os.remove(f"{Rinex_file}.Z")
            print(f"{decompressed_path} Successfully decompressed.")

        # Download and Decompress the .gz file if it exists
        elif Rinex_file + ".gz" in files:
            print("The file can be foud on the CDDIS NASA website : 'gdc.cddis.eosdis.nasa.gov' ")
            print(f"ftp://{ftp_host}{ftp_path}")
            print(f"The RINEX file name : {Rinex_file}.Z ")
            ftp.retrbinary(f"RETR {Rinex_file}.gz", open(f"{Rinex_file}.gz", 'wb').write)
            with gzip.open(f"{Rinex_file}.gz", 'rb') as f_in:
                with open(f"{Rinex_file}", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(f"{Rinex_file}.gz")
            print(f"{Rinex_file}.gz successfully downloaded")
            print(f"{Rinex_file}.gz successfully decompressed")


        else:
            print(f"The file {Rinex_file} does not exist.")

        ftp.quit()


        # import the Rinex file in Skydel
    
        # Get the current working directory
        current_dir = os.getcwd()

        # Look for the Rinex file in a subdirectory of the current working directory
        rinex_dir = os.path.join(current_dir, "")
        path = os.path.join(rinex_dir, local_path)

        rinex = sim.call(ImportConstellationParameters("GPS", path, 0, "Default"))
    except UnicodeDecodeError :
        pass
    print("{} Successfully imported in Skydel".format(Rinex_file))


#if the signal is a  Galileo
if "E1" in sig:
    print ("======================================================================================================")
    print("The signal is a Galileo")
    try :
        
        # last forler where the Rinex is located = YY+l
        new_year = ""
        for i in range(len(str(year))):
            if i !=1 & i !=2:
                new_year = new_year  + str(year)[i]   
                dossier = new_year + "l"
                     
        Rinex_file = "BRDC00CNS_R_"+ str(year)+ str(Day)+"0000"+"_"+"01"+ "D_EN.rnx.gz"
        try :
        # Download the RINEX file 
            link =   'ftp://serenad-public.cnes.fr/SERENAD0/FROM_NTMFV2/NAV/'+str(year)+ '/'+ str(Day)+'/'+ Rinex_file 
            with closing(request.urlopen(link)) as r:
                with open(Rinex_file, 'wb') as f:
                    shutil.copyfileobj(r, f)
            print("The file can be found on the CNES website : 'serenad-public.cnes.fr'")
            print(link)
            print("The rinex file name : {}".format(Rinex_file))
            print("{} successfully downloaded".format(Rinex_file))
            
        # Unzip the rinex file  
            file_unzip = "BRDC00CNS_R_"+ str(year)+ str(Day)+"0000"+"_"+"01"+ "D_EN.rnx"
            
            with gzip.open(Rinex_file, 'rb') as f_in:
                with open(file_unzip, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(Rinex_file)
            print("{} Successfully decompressed ".format(Rinex_file))

            
        #import the Rinex file in Skydel
        
            # Get the current working directory
            current_dir = os.getcwd()

            # Look for the Rinex file in a subdirectory of the current working directory
            rinex_dir = os.path.join(current_dir, "")
            path = os.path.join(rinex_dir, file_unzip)

            rinex = sim.call(ImportConstellationParameters("Galileo", path, 0, "Default"))
            print("{} Successfully imported in Skydel".format(Rinex_file))

        except :
            print("The Rinex file does not exist on the servor ftp")
            
            
    except UnicodeDecodeError :
            pass
  


#if the signal is a  Glonass
if "G1" in sig:
    print ("======================================================================================================")
    print("The signal is a glonass")
    
    
    try :
        # last forler where the Rinex is located = YY+g
        new_year = ""
        for i in range(len(str(year))):
            if i !=1 & i !=2:
                new_year = new_year  + str(year)[i] 
                dossier = new_year + "g"
                
    
        ftp_host = 'gdc.cddis.eosdis.nasa.gov'
        ftp_path = '/pub/gps/data/daily/'+ str(year) + '/' + str(Day) + '/' + dossier 
        local_path = "brdc"+ str(Day)+str(0)+"."+str(dossier)

        ftp = FTP_TLS(ftp_host)
        ftp.login()
        ftp.prot_p()
        ftp.cwd(ftp_path)
        files = ftp.nlst()
        Rinex_file = "brdc"+ str(Day)+str(0)+"."+str(dossier)

                
        # Download .Z file if it exists
        if Rinex_file + ".Z" in files:
            print ("The file can be found on the NASA CDDIS website: 'gdc.cddis.eosdis.nasa.gov'")
            print(f"ftp://{ftp_host}{ftp_path}")
            with open(Rinex_file + ".Z", 'wb') as f:
                ftp.retrbinary(f"RETR {Rinex_file}.Z", f.write)
            print(f"The rinex file name : {Rinex_file}.Z")
            print(f"{Rinex_file}.Z successfully downloaded.")

            # Decompress the .Z file
            compressed_path = local_path + ".Z"
            decompressed_path = local_path
            with open(decompressed_path, 'wb') as f_out:
                with open(compressed_path, 'rb') as f_in:
                    decompressed_data = unlzw3.unlzw(f_in.read())
                    f_out.write(decompressed_data)
            print(f"{decompressed_path} successfully decompressed.")
            os.remove(f"{Rinex_file}.Z")


        # Download and Decompress the .gz file if it exists
        elif Rinex_file + ".gz" in files:
            ftp.retrbinary(f"RETR {Rinex_file}.gz", open(f"{Rinex_file}.gz", 'wb').write)
            print("The file can be foud on the CDDIS NASA website : 'gdc.cddis.eosdis.nasa.gov'")
            print(f"ftp://{ftp_host}{ftp_path}")
            with gzip.open(f"{Rinex_file}.gz", 'rb') as f_in:
                with open(f"{Rinex_file}", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"The RINEX file name : {Rinex_file}.gz")
            os.remove(f"{Rinex_file}.gz")
            print(f"{Rinex_file}.gz successfully downloaded")
            print(f"{Rinex_file}.gz successfully decompressed")

        else:
            print(f"The file {Rinex_file} does not exist on the server ftp")

        ftp.quit()

        #import the Rinex file in Skydel
    
       # Get the current working directory
        current_dir = os.getcwd()

        # Look for the Rinex file in a subdirectory of the current working directory
        rinex_dir = os.path.join(current_dir, "")
        path = os.path.join(rinex_dir, local_path)

        rinex = sim.call(ImportConstellationParameters("GLONASS", path, 0, "Default"))
        print("{} Successfully imported in Skydel".format(Rinex_file))

    except (FileNotFoundError, ftplib.error_perm):
            print("The RINEX file does not exist on the server ftp")
    except UnicodeDecodeError :
        pass


#if the signal is a beidou
if "B1" in sig:
    print ("======================================================================================================")
    print("The signal is a beidou")
    
    try :
        # last forler where the Rinex is located = YY+f
        new_year = ""
        for i in range(len(str(year))):
            if i !=1 & i !=2:
                new_year = new_year  + str(year)[i]    
                folder = new_year + "f"
    
        Rinex_file = "ABPO00MDG_R_"+ str(year)+str(Day)+"0000_01D_CN.rnx.gz"
                
    # Download the RINEX file 
        try:
            with FTP_TLS('gdc.cddis.eosdis.nasa.gov') as f:
                f.login()
                f.prot_p()
                with open(Rinex_file, 'wb') as o:              
                    link = '/pub/gps/data/daily/' + str(year) + '/' + str(Day) + '/' + folder + '/' + Rinex_file
                    f.retrbinary(f"RETR {link}", o.write)
                Rinex_file = "ABPO00MDG_R_"+ str(year)+str(Day)+"0000_01D_CN.rnx.gz"
                print("The file can be found on the CDDIS NASA website: 'gdc.cddis.eosdis.nasa.gov'")
                print(f"ftp ://gdc.cddis.eosdis.nasa.gov{link}")
                print("The rinex file name : {}".format(Rinex_file)) 
                print("{} successfully downloaded".format(Rinex_file))

            #Unzip the rinex file
            Rinex_file_unzip = "brdc"+ str(Day)+str(0)+"."+str(folder)
            with gzip.open(Rinex_file, 'rb') as f_in:
                with open(Rinex_file_unzip, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(Rinex_file)
            print("{} Successfully decompressed ".format(Rinex_file))

            #import the Rinex file in Skydel
            # Get the current working directory
            current_dir = os.getcwd()

            # Look for the Rinex file in a subdirectory of the current working directory
            rinex_dir = os.path.join(current_dir, "")
            path = os.path.join(rinex_dir, Rinex_file_unzip)

            rinex = sim.call(ImportConstellationParameters("Beidou", path, 0, "Default"))
            print("{} Successfully imported in Skydel".format(Rinex_file))

        except (FileNotFoundError, ftplib.error_perm):
            print("The RINEX file does not exist on the server ftp")
            exit()
        
    except UnicodeDecodeError:
        pass

print()
print("                            ********                                   ")      
print("Great now you can continue your simulation on Skydel!!!")


    




