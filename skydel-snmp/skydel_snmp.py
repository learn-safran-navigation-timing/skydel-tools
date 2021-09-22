#!/usr/bin/python3
#skydel-snmp-python file with formal MIB enterprise OROLIA - V5 and Higher
#use this file to learn how snmp is managed for your GSG8 with few examples 
#and customize your other commands by using new cmd calls
# --------------------------------------------------------------------------
from snmp_pass import *
import sys
from skydelsdx.remotesimulator import *
from skydelsdx.commands import *

snmp = SnmpPass(".1.3.6.1.4.1.18837.3.5")

# ---------------------------------------------
# List of commands for driving GSG8/SKYDEL
# ---------------------------------------------
# is_running() GET: allows to check if SKYDEL scenario has been started or not. 
# is-running() SET : allows to start or stop Skydel scenario
#
# "Next custom snmp cmd to create" : 
# Enter new-cmd() : description
# Enter new-cmd() : description
# Enter new-cmd() : description
##
# ---------------------------------------------  
def is_running():
  result = ('integer', 0)
  try:
    sim = RemoteSimulator()
    sim.connect()
    if sim.call(GetSimulatorState()).stateId() == SimulatorState.StateStarted:
      result = ('integer', 1)
  except:
    pass
  return result

def set_running(t, value):
  if t != 'integer':
    raise SnmpSetWrongType()
  value = int(value)
  if value < 0 or value > 1:
    raise SnmpSetWrongValue()
  try:
    sim = RemoteSimulator()
    sim.connect()
    if sim.call(GetSimulatorState()).stateId() == SimulatorState.StateStarted:
      if value == 0:
        sim.stop()
    else:
      if value == 1:
        sim.start()
  except:
    raise SnmpSetNotWritable()
	
#---------------------------------------------

#--------------------------------------------------------------  
#--  cmd calls creating link according OID/MIB organisation  --
#--------------------------------------------------------------
# select a new custom cmd by removing '#' 
#--------------------------------------------------------------


#OID .1.3.6.1.4.1.18837.3.5.1.0 "SKYDEL is Running ? + set/get"
snmp.add_custom_entry(".1.0", is_running, set_running)
#OID .1.3.6.1.4.1.18837.3.5.2.0 "Next custom snmp cmd to create" 
#snmp.add_custom_entry(".2.0", get_tobedef, set_tobedef)
#OID .1.3.6.1.4.1.18837.3.5.2.0 "Next custom snmp cmd to create" 
#
#snmp.add_custom_entry(".3.0", get_tobedef, set_tobedef)
#snmp.add_custom_entry(".4.0", get_tobedef, set_tobedef)
#snmp.add_custom_entry(".5.0", get_tobedef, set_tobedef)
#---------------------------------------------------------------

snmp.run_passthrough(sys.argv)
#snmp.run_persist()

