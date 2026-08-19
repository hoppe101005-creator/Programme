from ctypes import *

epos = windll.LoadLibrary(r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll")

print ("Epos Command Library geladen")

error_code = c_uint()

handle = epos.VCS_OpenDevice(b"EPOS4", b"MAXON SERIAL V2", b"USB", b"USB0", byref(error_code))

print (handle)
print ("Error code: ", error_code.value)
