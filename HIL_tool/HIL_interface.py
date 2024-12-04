from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QCheckBox, QComboBox, QDateTimeEdit, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import skydelsdx
import sys 
from skydelsdx.commands import *
from skydelsdx.units import *
import keyboard
import datetime
import time


if sys.platform == "win32":
  BUSY_WAIT_DURATION_MS = 15.
else:
  BUSY_WAIT_DURATION_MS = 1.


class SectionFrame(QWidget):
    def __init__(self, title, elements, parent=None):
        super().__init__(parent)

        self.error_message = QLabel()  # QLabel pour afficher l'avertissement
        self.error_message.setStyleSheet("color: red; font-weight: bold;")
        self.title = title

        section_label = QLabel(title)
        section_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        layout = QVBoxLayout()
        layout.addWidget(section_label)

        self.widgets = {}  # Stocker une référence aux widgets pour accéder à leurs valeurs ultérieurement

        for label_text, widget_type, widget_args in elements:
            label = QLabel(label_text)

            # Gérer spécifiquement le cas de QDateTimeEdit
            if issubclass(widget_type, QDateTimeEdit):
                widget = widget_type()
                widget.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
                widget.setCalendarPopup(True)
            elif issubclass(widget_type, QComboBox):
                values = widget_args.get("values", [])
                default_value = widget_args.get("default", "")

                widget = widget_type()
                widget.addItems(values)

                if default_value in values:
                    widget.setCurrentText(default_value)
                    
            # Gérer spécifiquement le cas de QLineEdit
            elif issubclass(widget_type, QLineEdit):
                widget = widget_type()
                default_text = widget_args.get("default", "")
                widget.setText(default_text)
                
            else:
                widget = widget_type(self, **widget_args)

            layout.addWidget(label)
            layout.addWidget(widget)
            
            # Stocker la référence au widget
            self.widgets[label_text] = widget

        # Ajouter le QLabel pour l'avertissement
        layout.addWidget(self.error_message)

        self.setLayout(layout)

    def validate_inputs(self):
        validated = False
        tjoin_widget = self.widgets.get("Tjoin ( > Time between positions + Engine Latency):")
        try:
            tjoin = int(tjoin_widget.text())
            time_between_positions = int(self.widgets["Time between positions (in ms):"].text())
            engine_latency = int(self.widgets["Engine Latency (in ms):"].text())

            if tjoin < time_between_positions + engine_latency:
                # Afficher l'avertissement dans le QLabel
                self.error_message.setText("Warning : Tjoin must be greater than Time between positions + Engine Latency.")
            else:
                # Effacer l'avertissement s'il n'est plus nécessaire
                self.error_message.clear()
                validated = True
            
        except:
            self.error_message.setText("Warning : Enter values above.")
            
        return validated
            
    def show_widgets(self):
        for widget in self.widgets.values():
            widget.setVisible(True)
        self.setVisible(True)

    def hide_widgets(self):
        for widget in self.widgets.values():
            widget.setVisible(False)
            widget.setChecked(False)
        self.setVisible(False)

class SkydelScenario(QWidget):
    def __init__(self, hardware, radiocard, dateTime, isInterf, isSpoof, hil_vehicle, simDurationMs, syncDurationMs):
        super().__init__()

        self.hardware = hardware
        self.radiocard = radiocard
        self.isInterf = isInterf
        self.isSpoof = isSpoof
        self.hil_vehicle = hil_vehicle 
        self.simDurationMs = simDurationMs
        self.syncDurationMs = syncDurationMs
        self.dateTime = dateTime
        
        self.sim = skydelsdx.RemoteSimulator()

    def SetScenario(self, ipAdress, EngineLatencyMs, hilTjoin):
        # Connect scenario
        self.sim.setVerbose(True)
        self.sim.connect(ipAdress) 
        
        if self.hardware == "None":
            if ipAdress != "localhost":
              error("Can't run this script on a different computer if the OS time isn't in sync with the radio's PPS.")

        # Check the engine latency (Skydel's system wide preference)
        if self.sim.call(GetEngineLatency()).latency() != EngineLatencyMs:
          self.sim.call(SetEngineLatency(EngineLatencyMs))  # Uncomment this line to set the engine latency preference

        # Check the streaming buffer preference, do not change it from its default value
        if self.sim.call(GetStreamingBuffer()).size() != 200:
          error("Please do not change the Streaming Buffer preference.")
          
        ######################## Main config ##################  
        
        # Create new config, ignore the default config if it's set
        self.sim.call(New(True, True))
       
        #Apply scenario
        self.setMain(hilTjoin)
            

    def setMain(self, hilTjoin):
        self.sim.call(SetModulationTarget(self.radiocard, "", "0", True, "MainId"))
        self.sim.call(ChangeModulationTargetSignals(0, 12500000, 100000000, "UpperL", "L1CA, E1", -1, False, "MainId"))
        self.sim.call(SetVehicleTrajectoryFixEcef("Fix", 4221355.11358025577, -111321.210075403797, 4763976.24896331131, 0, 0, 0))
        self.sim.call(SetGpsStartTime(datetime.datetime(int(self.dateTime[:4]), int(self.dateTime[5:7]), int(self.dateTime[8:10]), int(self.dateTime[11:13]), int(self.dateTime[14:16]), int(self.dateTime[17:19]))))
        
        self.sim.call(EnableLogRaw(False))  # You can enable raw logging and compare the logs (the receiver position is especially helpful)
        self.sim.call(EnableLogHILInput(False))  # This will give you exactly what Skydel has received through the HIL interface
        
        # HIL Tjoin is a volatile parameter that must be set before every HIL simulation
        self.sim.call(SetHilTjoin(hilTjoin))
        
        if self.isInterf:
            self.sim.call(SetModulationTarget(self.radiocard, "", "1", True, "interference"))
            self.sim.call(ChangeModulationTargetInterference(0, 12500000, 85000000, 1, 1575420000, 30, "interference", "L1CA,E1"))
            
            self.sim.call(AddIntTx("Transmitter 1", True, 1, True, -50, "first_interf"))
            self.sim.call(SetIntTxCW(True, 1575420000, 0, "first_interf", "CW_interf", 0, None))
            self.sim.call(SetIntTxFixEcef(4221360.22912330739, -111457.832341467962, 4763968.5733548915, 0, 0, 0, "first_interf"))
        
        if self.isSpoof and not self.isInterf:
            self.sim.call(SetModulationTarget(self.radiocard, "", "1", True, "interference"))
            self.sim.call(ChangeModulationTargetInterference(0, 12500000, 85000000, 1, 1575420000, 30, "interference", "L1CA,E1"))
            
            self.sim.call(AddSpoofTx("Spoofer 1", False, "127.0.0.1", 1, "spoofer"))
            self.sim.call(SetSpoofTxFixEcef(4221399.88472, -111256.34324, 4763938.34769, 0, 0, 0, "spoofer"))
            self.sim.call(SetSpoofTxRefPower(-20, "spoofer"))
            
            self.setSpoofer()
            
        elif self.isSpoof and self.isInterf:
            self.sim.call(AddSpoofTx("Spoofer 1", False, "127.0.0.1", 1, "spoofer"))
            self.sim.call(SetSpoofTxFixEcef(4221399.88472, -111256.34324, 4763938.34769, 0, 0, 0, "spoofer"))
            self.sim.call(SetSpoofTxRefPower(-20, "spoofer"))
            #self.sim.call(SetSpoofTxHil("spoofer"))
            
            self.setSpoofer()

        ######### Set HIL vehicle #########
        
        if self.hil_vehicle == "Main":
            self.sim.call(SetVehicleTrajectory("HIL"))
            
        elif self.hil_vehicle == "Spoofer" and self.isInterf:
            self.sim.call(AddSpoofTx("Spoofer 1", False, "127.0.0.1", 1, "spoofer"))
            self.sim.call(SetSpoofTxRefPower(-20, "spoofer"))
            self.sim.call(SetSpoofTxHil("spoofer"))
            self.setSpoofer()
            
        elif self.hil_vehicle == "Spoofer" and not self.isInterf:
            self.sim.call(SetModulationTarget(self.radiocard, "", "1", True, "interference"))
            self.sim.call(ChangeModulationTargetInterference(0, 12500000, 85000000, 1, 1575420000, 30, "interference", "L1CA,E1"))
            
            self.sim.call(AddSpoofTx("Spoofer 1", False, "127.0.0.1", 1, "spoofer"))
            self.sim.call(SetSpoofTxRefPower(-20, "spoofer"))
            self.sim.call(SetSpoofTxHil("spoofer"))
            self.setSpoofer()
            
        elif self.hil_vehicle == "Interference" and self.isSpoof:
            self.sim.call(AddIntTx("Transmitter 1", True, 1, True, -50, "first_interf"))
            self.sim.call(SetIntTxCW(True, 1575420000, 0, "first_interf", "CW_interf", 0, None))
            self.sim.call(SetIntTxHil("first_interf"))
            
        elif self.hil_vehicle == "Interference" and not self.isSpoof:
            self.sim.call(SetModulationTarget(self.radiocard, "", "1", True, "interference"))
            self.sim.call(ChangeModulationTargetInterference(0, 12500000, 85000000, 1, 1575420000, 30, "interference", "L1CA,E1"))
            
            self.sim.call(AddIntTx("Transmitter 1", True, 1, True, -50, "first_interf"))
            self.sim.call(SetIntTxCW(True, 1575420000, 0, "first_interf", "CW_interf", 0, None))
            self.sim.call(SetIntTxHil("first_interf")) 

        # The streaming check is performed at the end of pushEcefNed. It's recommended to disable this check 
        # and do it asynchronously outside of the while loop when sending positions at high frequencies.
        self.sim.setHilStreamingCheckEnabled(True)
        self.sim.beginVehicleInfo()
        # Enable the PPS synchronisation
        self.sim.call(EnableMainInstanceSync(True))
    
    
    def setSpoofer(self):
        
        spoof = skydelsdx.RemoteSpooferSimulator()
        spoof.connect("localhost", 1) 
        spoof.call(New(True, True))

        spoof.call(SetModulationTarget("Spoofer", "", "", True, "spoofcard"))
        spoof.call(ChangeModulationTargetSignals(0, 1250000, 125000000, "UpperL", "L1CA,E1", 0, False, "spoofcard", None))
        spoof.call(SetVehicleTrajectory("Circular"))
        spoof.call(SetVehicleTrajectoryCircular("Circular", 0.848858624899152758, -0.0263789632123759693, 2, 200, 3, True, 0))
        spoof.call(SetGpsStartTime(datetime.datetime(int(self.dateTime[:4]), int(self.dateTime[5:7]), int(self.dateTime[8:10]), int(self.dateTime[11:13]), int(self.dateTime[14:16]), int(self.dateTime[17:19]))))

        
    def getsimDurationMs(self):
        return self.simDurationMs
    
    def getsyncDurationMs(self):
        return self.syncDurationMs
    
    def getSim(self):
        return self.sim

class Key_board(QWidget):
    def __init__(self):
        super().__init__()
        self.lastPosLAT = 0
        self.lastPosLON = 0
        self.speed = 0 #Value from 0 to 5
        self.number = 0
        
    def KeyMove(self, position):
        # Vehicule speed change

        if keyboard.is_pressed('a')==True:
            if self.number >= 6:
                self.number = 0
                if self.speed < 4:
                    self.speed += 0.05
                    self.speed = round(self.speed, 2)
            else:
                self.number += 1
        elif keyboard.is_pressed('s')==True:
            if self.number >= 6:
                self.number = 0
                if self.speed >= 0.05:
                    self.speed -= 0.05
                    self.speed = round(self.speed, 2)
            else:
                self.number += 1

        if keyboard.is_pressed('left')==True:
            if keyboard.is_pressed('down')==True:
                position.lon -= 0.0000005*self.speed
                position.lat -= 0.0000005*self.speed
                self.lastPosLAT = -0.5
                self.lastPosLON = -0.5
            elif keyboard.is_pressed('up')==True: 
                position.lon -= 0.0000005*self.speed
                position.lat += 0.0000005*self.speed
                self.lastPosLAT = 0.5
                self.lastPosLON = -0.5
            else:
                position.lon -= 0.000001*self.speed
                self.lastPosLAT = 0
                self.lastPosLON = -1
        elif keyboard.is_pressed('right')==True:   
            if keyboard.is_pressed('down')==True:
                position.lon += 0.0000005*self.speed
                position.lat -= 0.0000005*self.speed
                self.lastPosLAT = -0.5
                self.lastPosLON = 0.5
            elif keyboard.is_pressed('up')==True:
                position.lon += 0.0000005*self.speed
                position.lat += 0.0000005*self.speed
                self.lastPosLAT = 0.5
                self.lastPosLON = 0.5
            else:
                position.lon += 0.000001*self.speed
                self.lastPosLAT = 0
                self.lastPosLON = 1
                
        else:
            if keyboard.is_pressed('down')==True:
                position.lat -= 0.000001*self.speed
                self.lastPosLAT = -1
                self.lastPosLON = 0
            elif keyboard.is_pressed('up')==True: 
                position.lat += 0.000001*self.speed
                self.lastPosLAT = 1
                self.lastPosLON = 0
            else:
                position.lon += 0.000001*self.lastPosLON*self.speed
                position.lat += 0.000001*self.lastPosLAT*self.speed


class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HIL simulation")
        self.setGeometry(100, 100, 800, 600)
        # self.setStyleSheet("background-color: grey; color: white; border: 1px solid white;")

        # IP config
        self.ip_frame = SectionFrame("Skydel IP configuration", [
            ("IP address of Skydel:", QLineEdit, {"default": "localhost"})
        ])
        
        # Skydel Scenario
        self.skydel_frame = SectionFrame("Skydel Scenario configuration", [
            ("System:", QComboBox, {"values": ["GSG-7", "GSG-8", "None"]}),
            ("Output card:", QComboBox, {"values": ["NoneRT", "DTA-2115B", "DTA-2116"]}),
            ("HIL controlled vehicle:", QComboBox, {"values": ["Main", "Spoofer", "Interference"]}),
            ("Date and time:", QDateTimeEdit, {})
        ])
        
        # Skydel Scenario
        self.main_frame = SectionFrame("Main configuration", [
            ("Add a jammer", QCheckBox, {}),
            ("Add a spoofer", QCheckBox, {})
        ])
        
        # Skydel Scenario
        self.interference_frame = SectionFrame("Interference configuration", [
            ("Add a spoofer", QCheckBox, {})
        ])
        
        # Skydel Scenario
        self.spoofer_frame = SectionFrame("Spoofer configuration", [
            ("Add a jammer", QCheckBox, {})
        ])

        # HIL Parameters
        self.hil_params_frame = SectionFrame("HIL Parameters", [
            ("Tjoin ( > Time between positions + Engine Latency):", QLineEdit, {"default":"65"}),
            ("Time between positions (in ms):", QLineEdit, {"default":"15"}),
            ("Engine Latency (in ms):", QLineEdit, {"default":"45"})
        ])

        # Connecter le signal de changement de la combobox à la fonction de gestion
        self.skydel_frame.widgets["HIL controlled vehicle:"].currentIndexChanged.connect(self.handle_vehicle_selection)

        # Submit Button
        submit_button = QPushButton("Run", self)
        submit_button.clicked.connect(self.validate_and_submit)

        layout = QVBoxLayout()
        layout.addWidget(self.ip_frame)
        layout.addWidget(self.skydel_frame)
        layout.addWidget(self.main_frame)
        layout.addWidget(self.interference_frame)
        layout.addWidget(self.spoofer_frame)
        layout.addWidget(self.hil_params_frame)
        layout.addWidget(submit_button)
        

        self.setLayout(layout)
        
        self.spoofer_frame.hide_widgets()
        self.interference_frame.hide_widgets()

        
    def displayHilExtrapolationWarnings(sim):
      isVerbose = sim.isVerbose()
      sim.setVerbose(False)
      result = sim.call(GetHilExtrapolationState())
      if result.state() == HilExtrapolationState.NonDeterministic:
        print("Warning: HIL non deterministic extrapolation at millisecond", result.elapsedTime())
      elif result.state() == HilExtrapolationState.Snap:
        print("Warning: HIL position snap at millisecond", result.elapsedTime())
      sim.setVerbose(isVerbose)

    def validate_and_submit(self):
        # Valider les entrées avant de soumettre
        for frame in self.findChildren(SectionFrame):
            if frame.title == "HIL Parameters":
                validated = frame.validate_inputs()
                
                
        if validated:        
            ############## Set up the Scenario ##############   
            #Get values choosen
            skydelIpAddress = self.ip_frame.widgets["IP address of Skydel:"].text()
            systemType = self.skydel_frame.widgets["System:"].currentText()
            radioType = self.skydel_frame.widgets["Output card:"].currentText()
            HIL_vehicle = self.skydel_frame.widgets["HIL controlled vehicle:"].currentText()
            dateTime = self.skydel_frame.widgets["Date and time:"].dateTime()
            date_string = dateTime.toString(self.skydel_frame.widgets["Date and time:"].displayFormat())
            hilTjoin = int(self.hil_params_frame.widgets["Tjoin ( > Time between positions + Engine Latency):"].text())
            timeBetweenPosMs = int(self.hil_params_frame.widgets["Time between positions (in ms):"].text())
            skydelEngineLatencyMs = int(self.hil_params_frame.widgets["Engine Latency (in ms):"].text())
            jam_main = self.main_frame.widgets["Add a jammer"].isChecked()
            spoof_main = self.main_frame.widgets["Add a spoofer"].isChecked()
            spoof_int = self.interference_frame.widgets["Add a spoofer"].isChecked()
            jam_spoof = self.spoofer_frame.widgets["Add a jammer"].isChecked()
            
            isJam = jam_main or jam_spoof
            isSpoof = spoof_int or spoof_main
            
            if HIL_vehicle == "Spoofer":
                vehicle_dest = "spoofer"
            elif HIL_vehicle == "Interference":
                vehicle_dest = "first_interf"
            else:
                vehicle_dest = ""
            
            print(skydelIpAddress, radioType, HIL_vehicle, dateTime, date_string, hilTjoin, timeBetweenPosMs, skydelEngineLatencyMs, jam_main, spoof_int)
            
            # Set Scenario
            #trajectory = StraightTrajectory(speed=0.1)
            
            scenariohil = SkydelScenario(systemType, radioType, date_string, isJam, isSpoof, HIL_vehicle, 6000000, 2000)
            
            scenariohil.SetScenario(skydelIpAddress, skydelEngineLatencyMs, hilTjoin)
            
            sim = scenariohil.getSim()
            
            Keyboard_type = Key_board()
    
    
            # From here we want to make sure to stop the simulation if something goes wrong
            try:
            
              # Arm the simulator, when this command returns, we can start synchronizing with the PPS
              sim.call(ArmPPS())
    
              # The WaitAndResetPPS command returns immediately after a PPS signal, which is our PPS reference (PPS0)
              sim.call(WaitAndResetPPS())
    
              # If our PC clock is synchronized with the PPS, the nearest rounded second is the PPS0
              if systemType != "None":
                  pps0TimestampMs = getClosestPpsTimeMs()
                  
              # The command StartPPS will start the simulation at PPS0 + syncDurationMs
              # You can synchronize with your HIL simulation start, by changing the value of syncDurationMs (resolution in milliseconds)
              sim.call(StartPPS(scenariohil.getsyncDurationMs()))
              
              # If the PC clock is NOT synchronized with the PPS, we can ask Skydel to tell us the PC time corresponding to PPS0
              if systemType == "None":
                  pps0TimestampMs = sim.call(GetComputerSystemTimeSinceEpochAtPps0()).milliseconds()
    
              # Compute the timestamp at the beginning of the simulation
              simStartTimestampMs = pps0TimestampMs + scenariohil.getsyncDurationMs()
            
              # We send the first position outside of the loop, so initialize this variable for the second position
              nextTimestampMs = simStartTimestampMs + timeBetweenPosMs
    
              # Keep track of the simulation elapsed time in milliseconds
              elapsedMs = 0.0
              warningTimeMs = 0.0
    
              # Fix a precise attitude
              fixedAttitude = Attitude(toRadian(0), toRadian(0), 0)
              angularVelocity = Attitude(0.0, 0.0, 0.0)
      
              # Skydel must know the initial position of the receiver for initialization.
              # Use pushLla, pushEcef or pushEcefNed based on your requirements.
              position = Lla(toRadian(48.66821283), toRadian(-1.49932456), 1.0)
              position = position.addEnu(Enu(0.6, 0.8, 0))
              positionECEF = position.toEcef()
              
              sim.pushEcefNed(elapsedMs, positionECEF,fixedAttitude, dest = vehicle_dest)
              
              
              # Send positions in real time until the elapsed time reaches the desired simulation duration
              while True:
                # Wait for the next position's timestamp
                preciseSleepUntilMs(nextTimestampMs)
                nextTimestampMs += timeBetweenPosMs
    
                # Get the current elapsed time in milliseconds
                elapsedMs = getCurrentTimeMs() - simStartTimestampMs

                Keyboard_type.KeyMove(position)        
    
                # Push the position to Skydel
                positionECEF = position.toEcef()
                sim.pushEcefNed(elapsedMs, positionECEF,fixedAttitude, dest = vehicle_dest)

                # It is recommended to do this check at 10 Hz or less to avoid TCP stack overflow.
                # Do this check asynchronously, outside of this loop, if you are sending positions at a high rate.
                # HIL uses UDP, so you can send positions at 100 Hz or 1000 Hz without any issues.
                if elapsedMs > warningTimeMs + 1000.0:
                  warningTimeMs = elapsedMs
                  #self.displayHilExtrapolationWarnings(sim)
    
            finally:
                # Stop the simulation
                sim.stop()
            
                # Disconnect from Skydel
                sim.disconnect()
       
        
                
    def handle_vehicle_selection(self):
        selected_vehicle = self.skydel_frame.widgets["HIL controlled vehicle:"].currentText()

        # Afficher ou masquer les widgets en fonction de la sélection du véhicule
        if selected_vehicle == "Interference":
            self.interference_frame.show_widgets()
            self.spoofer_frame.hide_widgets()
            self.main_frame.hide_widgets()
        elif selected_vehicle == "Spoofer":
            self.spoofer_frame.show_widgets()
            self.interference_frame.hide_widgets()
            self.main_frame.hide_widgets()
        else:
            self.spoofer_frame.hide_widgets()
            self.interference_frame.hide_widgets()
            self.main_frame.show_widgets()

        # Ajouter ici le code pour soumettre les données si la validation réussit
        
        
    def displayHilExtrapolationWarnings(self, sim):
      isVerbose = sim.isVerbose()
      sim.setVerbose(False)
      result = sim.call(GetHilExtrapolationState())
      if result.state() == HilExtrapolationState.NonDeterministic:
        print("Warning: HIL non deterministic extrapolation at millisecond", result.elapsedTime())
      elif result.state() == HilExtrapolationState.Snap:
        print("Warning: HIL position snap at millisecond", result.elapsedTime())
      sim.setVerbose(isVerbose)
      

# Get the system time in milliseconds
def getCurrentTimeMs():
  return time.time() * 1000.


# This implies your OS time is synced with the radio's PPS signal
def getClosestPpsTimeMs():
  return round(getCurrentTimeMs() / 1000.) * 1000.

# Sleep until a given timestamp
def preciseSleepUntilMs(timestampMs, busyWaitDurationMs = BUSY_WAIT_DURATION_MS):
  currentTimeMs = getCurrentTimeMs()

  # print(currentTimeMs, " ", timestampMs)
  # We already passed the timestamp
  if currentTimeMs > timestampMs:
    #òprint("Warning: tried to sleep to a timestamp in the past")
    return

  # Since time.sleep might not be super precise, we busy wait some period of time
  sleepDurationSec = (timestampMs - currentTimeMs - busyWaitDurationMs) / 1000.

  # If negative, we only busy wait
  if sleepDurationSec > 0:
    time.sleep(sleepDurationSec)

  # Busy wait until we reach our timestamp
  while getCurrentTimeMs() < timestampMs:
    pass


# Helper function to exit with an error message
def error(message):
  print(message)
  sys.exit(-1)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
