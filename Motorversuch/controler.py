import ctypes
from ctypes import *
from pathlib import Path

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS2\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = ctypes.WinDLL(dll_path)
class controler:
    def __init__(self):
        self.handle = None
        self.error_code = c_uint(0)
        self.node_id = 1


    def open_device(self):
        self.handle = epos.VCS_OpenDevice(
            b"EPOS4",
            b"MAXON SERIAL V2",
            b"USB",
            b"USB0",
            byref(self.error_code)
        )
        
        
    def pruefe_dateipfad(dateipfad):
        return Path(dateipfad).exists()


    def list_port_names():
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

    def list_interfaces():
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
            

    def list_protocols():
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


    def list_devices():
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


    def find_device():
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

    def fehlercode_ausgeben(error_code):
        buffer = create_string_buffer(256)
        
        epos.VCS_GetErrorInfo(
            error_code,
            buffer,
            256
        )

        print("Fehlermeldung: ", buffer.value.decode("latin1"))
        
    def rueckgabe():
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