from ctypes import *

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = Windll(dll_path)

print ("Epos Command Library geladen")
print(epos.VCS_GetDeviceNameSelection)
print ("VSC_OpenDevice gefunden: ", hasattr(epos, "VCS_OpenDevice"))

epos.VCS_GetErrorInfo.argtypes = [
    c_uint,
    c_char_p,
    c_uint
]

epos.VCS_OpenDevice.argtypes = [
    c_char_p, 
    c_char_p, 
    c_char_p, 
    c_char_p, 
    POINTER(c_uint)
    ]

epos.VCS_OpenDevice.restype = c_ulonglong

error_code = c_uint(0)


handle = epos.VCS_OpenDevice(
    b"EPOS4", 
    b"MAXON Serial V2", 
    b"USB", 
    b"USB0", 
    byref(error_code)
    )

buffer = create_string_buffer(256)

epos.VCS_GetErrorInfo(error_code.value, buffer, 256)

print ("Handle: ", handle)
print ("Error code: ", error_code.value)
print ( "Fehlercode: ", buffer.value.decode("latin1"))
print (buffer.value.decode(errors="ignore"))
print ("Handle type: ", type(handle))