import machine
import utime

# 1. Pins am Raspberry Pi Pico definieren
# Verbinde GP2 mit PUL+ (Pulse) und GP3 mit DIR+ (Direction) am TB6600
PUL_PIN = 2
DIR_PIN = 3

# Pins als digitale Ausgänge konfigurieren
pul = machine.Pin(PUL_PIN, machine.Pin.OUT)
dir = machine.Pin(DIR_PIN, machine.Pin.OUT)

# 2. Einstellungen für deinen Schrittmotor & TB6600
# Ändere diesen Wert passend zu deiner DIP-Schalter-Einstellung am TB6600:
# Vollschritt = 200, 1/2 Schritt = 400, 1/4 Schritt = 800, 1/8 Schritt = 1600
SCHRITTE_PRO_UMDREHUNGEN = 200
UMDREHUNGEN = 5

# Geschwindigkeit: Pause zwischen den Pulsen in Sekunden (kleiner = schneller)
# Achtung: Zu kleine Werte (z. B. unter 0.0002) führen zum Blockieren des Motors!
GESCHWINDIGKEIT = 0.001
WARTEZEIT = 0.1

def drehe_motor(schritte, richtung):
    """
    Dreht den Motor um eine bestimmte Anzahl von Schritten in eine Richtung.
    richtung = 1 (im Uhrzeigersinn), richtung = 0 (gegen Uhrzeigersinn)
    """
    dir.value(richtung)
    
    for _ in range(schritte):
        pul.value(1)
        utime.sleep(GESCHWINDIGKEIT)
        pul.value(0)
        utime.sleep(GESCHWINDIGKEIT)

# --- HAUPTPROGRAMM (Endlosschleife) ---
while True:
    print("Drehe im Uhrzeigersinn...")
    drehe_motor(SCHRITTE_PRO_UMDREHUNGEN * UMDREHUNGEN, 1) # 1 volle Umdrehung
    utime.sleep (WARTEZEIT)
    
    print("Drehe im Uhrzeigersinn...")
    drehe_motor(SCHRITTE_PRO_UMDREHUNGEN * UMDREHUNGEN, 0) # 1 volle Umdrehung
    utime.sleep (WARTEZEIT)
    
