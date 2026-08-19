from ctypes import *

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = windll.LoadLibrary(dll_path)

print ("Epos DLL erfolgreich geladen!")

buffer1 = create_string_buffer(256)
buffer2 = create_string_buffer(256)
buffer3 = create_string_buffer(256)
buffer4 = create_string_buffer(256)
error = c_uint()

result1 = epos.VCS_GetDeviceNameSelection(1, buffer1, 256, byref(error))
result2 = epos.VCS_GetProtocolStackNameSelection(1, buffer2, 256, byref(error))
result3 =epos.VCS_GetInterfaceNameSelection(1, buffer3, 256, byref(error))
result4 = epos.VCS_GetPortNameSelection(1, buffer4, 256, byref(error))

print("Device Name:", result1)
print("Protocol Stack Name:", result2)
print("Interface  Name:", result3)
print("Port Name:", result4)
