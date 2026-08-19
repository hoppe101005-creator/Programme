import machine
import sys
import utime

# 1. Pins am Raspberry Pi Pico definieren
# Verbinde GP2 mit PUL+ (Pulse) und GP3 mit DIR+ (Direction) am TB6600
PUL_PIN = 2
DIR_PIN = 3
INTERRUPT_PIN = 16
ENA_PIN = 17
NOT_AUS_PIN = 15

# Pins als digitale Ausgänge konfigurieren
pul = machine.Pin(PUL_PIN, machine.Pin.OUT)
dir = machine.Pin(DIR_PIN, machine.Pin.OUT)
interrupt = machine.Pin(INTERRUPT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
ena = machine.Pin (ENA_PIN, machine.Pin.OUT)
Not_Aus = machine.Pin(NOT_AUS_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# 2. Einstellungen für deinen Schrittmotor & TB6600
# Ändere diesen Wert passend zu deiner DIP-Schalter-Einstellung am TB6600:
# Vollschritt = 200, 1/2 Schritt = 400, 1/4 Schritt = 800, 1/8 Schritt = 1600
SCHRITTE_PRO_UMDREHUNGEN = 200
UMDREHUNGEN = 5
ZYKLEN = 50

# Geschwindigkeit: Pause zwischen den Pulsen in Sekunden (kleiner = schneller)
# Achtung: Zu kleine Werte (z. B. unter 0.0002) führen zum Blockieren des Motors!
GESCHWINDIGKEIT = 0.001
BESCHLEUNIGUNG = 0.005

WARTEZEIT = 0.1

def drehe_motor(schritte, richtung):
    """
    Dreht den Motor um eine bestimmte Anzahl von Schritten in eine Richtung.
    richtung = 1 (im Uhrzeigersinn), richtung = 0 (gegen Uhrzeigersinn)
    """
    dir.value(richtung)
    
    for i in range(0.5/BESCHLEUNIGUNG):
        pul.value(1)
        utime.sleep(0.5-i*BESCHLEUNIGUNG)
        pul.value(0)
        ena.value(1)
        utime.sleep(0.5-i*BESCHLEUNIGUNG)
        ena.value(0)
    for i in range(schritte*5):
        pul.value(1)
        utime.sleep(GESCHWINDIGKEIT)
        pul.value(0)
        utime.sleep(GESCHWINDIGKEIT)
        
        
def not_aus(pin):
    while True:
        if Not_Aus.value()==0:
            ena.value(1)
            pul.value(0)
            print("NOT-AUS betätigt")
            print("Programm beenden")
            sys.exit()

# --- HAUPTPROGRAMM (Endlosschleife) ---
Not_Aus.irq(handler=not_aus, trigger=machine.Pin.IRQ_FALLING)
ena.value(1)
while True:
    if interrupt.value()==0:
        for i in range (ZYKLEN):
            ena.value(0)
            print("Drehe im Uhrzeigersinn...")
            drehe_motor(SCHRITTE_PRO_UMDREHUNGEN, 1) # 1 volle Umdrehung
            utime.sleep (WARTEZEIT)
        
            print("Drehe gegen den Uhrzeigersinn...")
            drehe_motor(SCHRITTE_PRO_UMDREHUNGEN, 0) # 1 volle Umdrehung
            utime.sleep (WARTEZEIT)

    ena.value(1)
    
