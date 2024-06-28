# SKYDEL - PYTHON / DOWNLINK-PARSER-UI

## This folder provide a User Interface for the utility script to parse the Skydel downlink navigation messages.

### Installation:
1) Make sure python is install (from version 3.8) or download the latest python version from https://www.python.org/downloads/.

2) Open a terminal and check the installation:
```python –version (or python3 –version for Linux platform)```

3) Install the python packages:
```pip install -r requirements.txt.```

4) Run the Downlink parser script:
```python main_ui.py```

### Usage:
1) To parse a Downlink logging, click "Select file".

2) Select the DECODER type (DECODED, ENCODED, PARTIAL)
3) Choose the Nav Message type ('GPS_LNAV', 'GPS_CNAV2', 'GPS_CNAV', 'GLONASS_NAV', 'GALILEO_INAV',
                        'GALILEO_FNAV', 'GALILEO_CNAV', 'BEIDOU_D1_NAV', 'BEIDOU_D2_NAV', 'BEIDOU_CNAV1',
                        'BEIDOU_CNAV2', 'SBAS_NAV', 'QZSS_LNAV', 'QZSS_SLAS', 'NAVIC_NAV')

4) Push the "Save Ouput File". A dialog box will open allowing the user to choose where to store the decoded downlink file.


### N.B: 
This code is compatible with Skydel release 24.4.1 only and can be modified for other Skydel versions.

See section below for more information regarding the downlink parser script.

***************************************************************************
This folder contains utility scripts for parsing downlink navigation messages.
In each constellation script, there are functions returning a dictionary containing keys with parameters names and their
informations.

Dictionary keys :
	'name'    : Name of the paramater.
	'range'   : Index of the parameter.
	'binary'  : Binary value of the parameter.
	'decimal' : Decimal value of the parameter.
	'unit'    : Unit of the parameter.
		
These dictionaries can be used to convert the hexadecimal navigation message data to a readable format.
The script 'decode_downlink.py' allows to easily decode an entire downlink file for supported navigation messages.


To decode the downlink of a Septentrio receiver you must :

	1) Add  ",,,,,,Navigation Message (Hex)," at the top of the file. "Navigation Message (Hex)" index correspond to
the index of the navigation message.

	2) For L1C, use this command (python3 decode_downlink.py PARTIAL GPS_CNAV2 INPUTFILE)

***************************************************************************