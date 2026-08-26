import ctypes
from ctypes import *
from pathlib import Path
import time

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS2\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = ctypes.WinDLL(dll_path)
class controler:
    def __init__(self):
        self.handle = None
        self.error_code = c_uint(0)
        self.enable = c_int()
        self.node_id = 1
        self.geschwindigkeit = 500
        self.geschwindigkeit_werte = []
        self.beschleunigung = 10000
        self.verzögerung = 10000
        self.fault = c_int()
        self.mode = c_byte()
        self.reached = c_int()
        self.position_geschlossen = 0                    ### Position, an der das NSE komplett geschlossen ist
        self.end_position_lose = 0                       ### Position, an der das NSE komplett geöffnet ist
        self.end_position_gespannt = 0                   ### Position, an der das NSE spannt
        self.position_werkstück_wechsel = 0

    def open_device(self):
        self.handle = epos.VCS_OpenDevice(
            b"EPOS4",
            b"MAXON SERIAL V2",
            b"USB",
            b"USB0",
            byref(self.error_code)     
        )
        handle = self.handle
        epos.VCS_OpenDevice.restype = c_void_p
        return handle
          
    def pruefe_dateipfad(self,dateipfad):
        return Path(dateipfad).exists()

    def list_port_names(self):
        buffer = create_string_buffer(256)
        end = c_int()
        error = c_uint()

        result = epos.VCS_GetPortNameSelection(
            b"EPOS4",
            b"MAXON SERIAL V2",
            b"USB",
            True,
            buffer,
            256,
            byref(end),
            byref(error)
    )

        while result:
            print("Port:", buffer.value.decode())

            result = epos.VCS_GetPortNameSelection(
                b"EPOS4",
                b"MAXON SERIAL V2",
                b"USB",
                False,
                buffer,
                256,
                byref(end),
                byref(error)
        )

    def list_interfaces(self):
        error = c_uint()
        end = c_int()
        buffer = create_string_buffer(256)

        # Interface-Namen für USB anzeigen

        result = epos.VCS_GetInterfaceNameSelection(
            b"EPOS4",
            b"MAXON SERIAL V2",
            True,
            buffer,
            256,
            byref(end),
            byref(error)
        )

        while result:
            print("Interface:", buffer.value.decode())

            result = epos.VCS_GetInterfaceNameSelection(
                b"EPOS4",
                b"MAXON SERIAL V2",
                False,
                buffer,
                256,
                byref(end),
                byref(error)
            )
           
    def list_protocols(self):
        name = create_string_buffer(256)
        end = c_int()
        error = c_uint()

        start = 1

        while True:

                result = epos.VCS_GetProtocolStackNameSelection(
                    b"EPOS4",
                    start,
                    name,
                    256,
                    byref(end),
                    byref(error)
                )

                if result == 0:
                    break

                print("Protocol:", name.value.decode())

                if end.value:
                    break

                start = 0

    def list_devices(self):
        name = create_string_buffer(256)
        end = c_int()
        error = c_uint()

        epos.VCS_GetDeviceNameSelection.argtypes = [
            c_ushort,
            c_char_p,
            c_ushort,
            POINTER(c_int),
            POINTER(c_uint)
        ]

        start = 1

        while True:

            result = epos.VCS_GetDeviceNameSelection(
                start,
                name,
                256,
                byref(end),
                byref(error)
            )

            if result == 0:
                break

            print("Device:", name.value.decode())

            if end.value:
                break

            start = 0

    def find_device(self):
        error = c_uint(0)

        device = create_string_buffer(64)
        protocol = create_string_buffer(64)
        interface = create_string_buffer(64)
        port = create_string_buffer(64)

        baudrate = c_uint()
        timeout = c_uint()
        nodeid = c_ushort()
        handle = c_void_p()

        result = epos.VCS_FindDeviceCommunicationSettings(
            byref(handle),
            device,
            protocol,
            interface,
            port,
            64,
            byref(baudrate),
            byref(timeout),
            byref(nodeid),
            1,
            byref(error)
        )

        buffer = create_string_buffer(256)

        epos.VCS_GetErrorInfo(
            error.value,
            buffer,
            256
        )

        print(buffer.value.decode())
        print("Result:", result)
        print("Handle:", handle.value)
        print("Device:", device.value.decode())
        print("Protocol:", protocol.value.decode())
        print("Interface:", interface.value.decode())
        print("Port:", port.value.decode())
        print("Baudrate:", baudrate.value)
        print("NodeID:", nodeid.value)
        print("Error:", error.value)
        return error

    def fehlercode_ausgeben(self):
        buffer = create_string_buffer(256)
        
        epos.VCS_GetErrorInfo(
            self.error_code,
            buffer,
            256
        )
        print("Fehlermeldung: ", buffer.value.decode("latin1"))
        
    def rueckgabe(self):
        error_code = c_uint(0)
        buffer = create_string_buffer(256)
        epos.VCS_GetErrorInfo(error_code.value, buffer, 256)
        print ("Handle: ", self.handle)
        print ("Handle repr: ", repr(self.handle))
        print ("Handle type: ", type(self.handle))
        print ("Error code: ", error_code.value)
        print ( "Fehlercode: ", buffer.value.decode("latin1"))
        print (buffer.value.decode(errors="ignore"))
        print("Der Pfad existiert: ", controler.pruefe_dateipfad(dll_path))
        controler.fehlercode_ausgeben(controler.find_device())
        controler.list_devices()
        controler.list_protocols()
        controler.list_interfaces()
        controler.list_port_names()
        
    def aktuelle_position_auslesen(self):
    #Funktionsdefinition
        epos.VCS_GetPositionIs.argtypes = [
            c_void_p,
            c_ushort,
            POINTER(c_int),
            POINTER(c_uint)
        ]

        epos.VCS_GetPositionIs.restype = c_int

        current_position = c_int()

        result = epos.VCS_GetPositionIs(
            self.handle,
            self.node_id,
            byref(current_position),
            byref(self.error_code)
        )

        if result:
            position = current_position.value
            print(f"Aktuelle Position: {position}")
            return position
        else:
            print(f"Fehler: {self.error_code.value}")
         
    def position_einlesen(self,dokument):
        with open (dokument, "r") as f:
            position = int(f.read())
            print(dokument, position)
            return position
        
    def position_speichern(self, position, dokument):
        with open(dokument, "w") as f:
                f.write(str(position))
                print("Position", position, "wurde in ", dokument, "gespeichert")
                
    def nse_zu_position_bewegen(self,zielposition, geschwindigkeit,beschleunigung, verzoegerung):
        self.konsole_leeren()
        start_pos = self.aktuelle_position_auslesen()
        
        print("Startposition",start_pos)
        print("Zielposition", zielposition)
        self.aktivieren_controler()
        self.fahr_parameter_setzen(geschwindigkeit, beschleunigung, verzoegerung)
        self.enable_set()
        self.enable_prüf()
        self.get_operation_mode()
        
        
        print("Fault:", self.fault_pruef())
        
        result = epos.VCS_MoveToPosition(
           self.handle,
           self.node_id,
           zielposition,
           1,
           1,
           byref(self.error_code)
        )
        print("Move Result: ", result)
        print("Error: ", self.error_code.value)
        
        ende_pos = self.aktuelle_position_auslesen()
        if zielposition == self.end_position_lose:
            self.position_speichern(zielposition, "end_position_lose.txt")
        if zielposition == self.end_position_gespannt:
            self.position_speichern(zielposition, "end_position_gespannt.txt")
        if zielposition == self.position_werkstück_wechsel:
            self.position_speichern(zielposition, "position_werkstück_wechsel.txt")
        if zielposition == self.position_geschlossen:
                    self.position_speichern(zielposition, "position_geschlossen.txt")
        print("Endposition: ", ende_pos)
       
    def enable_prüf(self):
        epos.VCS_GetEnableState(
            self.handle,
            self.node_id,
            byref(self.enable),
            byref(self.error_code)
            )
            
        print("Enabled:",self.enable.value)
    
    def enable_set(self):
        result = epos.VCS_SetEnableState(
            self.handle,
            self.node_id,
            byref(self.error_code)
        )
        
        print("Enabled:",result)
        
    def aktivieren_controler(self):
        epos.VCS_ActivateProfilePositionMode(
            self.handle,
            self.node_id,
            byref(self.error_code)
            ) 
        
    def fahr_parameter_setzen(self,geschwindigkeit, beschleunigung, verzoegerung):
        epos.VCS_SetPositionProfile(
            self.handle,
            self.node_id,
            geschwindigkeit,
            beschleunigung,
            verzoegerung,
            byref(self.error_code)
        )
        print("Geschwindigkeit:",geschwindigkeit)
        print("Beschleunigung:", beschleunigung)
        print("Verzögerung:", verzoegerung)
        print("Errorcode:", self.error_code)
        
    def fault_pruef(self):
        result = epos.VCS_GetFaultState(
            self.handle,
            self.node_id,
            byref(self.fault),
            byref(self.error_code)
        )
        
        print("Fault Result", result)
        print("Fault:", self.fault.value)
        print("Error:", self.error_code.value)
        
        return self.fault.value
    
    def get_operation_mode(self):
        result = epos.VCS_GetOperationMode(
            self.handle,
            self.node_id,
            byref(self.mode),
            byref(self.error_code)
        )

        print(" Operationsmodus Result:", result)
        print("Operationsmodus Mode:", self.mode.value)
        
    def farget_reached(self):
        result = epos.VCS_GetTargetReached(
            self.handle,
            self.node_id,
            byref(self.reached),
            byref(self.error_code)
        )
        
        print("Targetreached Result: ", result)
        print("TargetReached: ", self.reached.value)
        return self.reached.value
    
    def konsole_leeren(self):
        print("\033c", end="")
        
    def aktuelle_drehzahl_auslesen(self):
        epos.VCS_GetVelocityIs.argtypes = [
            c_void_p,
            c_ushort,
            POINTER(c_int),
            POINTER(c_uint)
        ]

        epos.VCS_GetVelocityIs.restype = c_int

        current_velocity = c_int()

        result = epos.VCS_GetVelocityIs(
            self.handle,
            self.node_id,
            byref(current_velocity),
            byref(self.error_code)
        )

        if result:
            print("Aktuelle Drehzahl:", current_velocity.value, "rpm")
            return int(current_velocity.value)
        else:
            print("Fehler:", self.error_code.value)
            return None
        
    def get_drehzahl_max(self):
        while True:
            self.geschwindigkeit_werte.append(self.aktuelle_drehzahl_auslesen())
            time.sleep(0.2)
            return max(self.geschwindigkeit_werte)
