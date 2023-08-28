# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import time
from datetime import datetime
from datetime import date
from skydelsdx import *
from skydelsdx.commands import *
from datetime import timedelta
import skydelsdx
from skydelsdx.units import Ecef
from skydelsdx.units import Lla
from skydelsdx.units import Attitude
from skydelsdx.units import toRadian
import csv
import sys
import codecs
import Era_glonass_parts as prt

print(
    """


      ###################### ERA-GLONASS TESTS ######################
      
          This is not an official test for checking a receiver 
          conformity to ERA-GLONASS. This was only meant to 
          help the user testing all the points of the norm with 
          his DUT. It is a guided script to help the user step 
          by step making tests on his receiver.
          
      ###############################################################
      
      
      """
)

# Start the test
start = input("Do you want to start? (Y/N) ")
while start != "Y" and start != "N":
    start = input("Do you want to start? (Y/N) ")

if start == "Y":
    prt.startpart()
else:
    print("No simulation started")
