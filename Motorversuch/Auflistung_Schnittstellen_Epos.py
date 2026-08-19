from time import sleep
from ctypes import *

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = windll.LoadLibrary(dll_path)

name = create_string_buffer(256)
end = c_int()

runde = 0
index = 6
error_code = c_uint()

epos.VCS_GetProtocolStackNameSelection.argtypes = [
c_ushort,
c_char_p,
c_uint,
POINTER(c_int),
POINTER(c_uint)
]

while True:
    for index in range(0, 255):
        for runde in range(0, 10):
            result = epos.VCS_GetProtocolStackNameSelection(
                index,
                name,
                256,
                byref(end),
                byref(error_code)
            )
            
            print("Index ", index,
                "| Name ", name.value.decode(errors="ignore"), 
                "| Error ", error_code.value)
            sleep(2)
            
            if result == 0:
                break
            
            print(index, name.value.decode())
            index += 1
        print("  ")
        runde += 1