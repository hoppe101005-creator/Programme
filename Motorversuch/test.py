import ctypes
from ctypes import *
from pathlib import Path
import subprocess

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS2\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = ctypes.WinDLL(dll_path)
try:
    print(epos.VCS_GetVelocityIs)
except Exception as e:
    print(e)

try:
    print(epos.VCS_GetObject)
except Exception as e:
    print(e)

try:
    print(epos.VCS_GetObjectEx)
except Exception as e:
    print(e)